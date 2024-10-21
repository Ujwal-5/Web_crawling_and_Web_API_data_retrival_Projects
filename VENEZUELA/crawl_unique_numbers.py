import requests
import re
import csv
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import itertools

# To store unique numbers and ensure thread safety
unique_numbers = set()
lock = Lock()

# Function to fetch data from a URL
def fetch_data(j):
    global unique_numbers
    i = 1  # Start with the first page

    while True:  # Continue until no numbers are found
        url = f"https://rncenlinea.snc.gob.ve/reportes/resultado_busqueda?nombre={j}&p=1&page={i}&search=NOMB"
        response = requests.get(url)
        
        # Regex pattern to match all numbers after '/planilla/index/' and before '?'
        pattern = r'/planilla/index/(\d+)\?'
        
        # Find all matching numbers using findall()
        matches = re.findall(pattern, response.text)

        if matches:
            with lock:  # Ensure thread safety while modifying the set
                unique_numbers.update(matches)
            print(f"Found {len(matches)} numbers for {j} on page {i}")
            i += 1  # Increment page number and continue fetching
        else:
            print(f"No numbers found for {j} on page {i}. Stopping...")
            break  # Stop fetching when no numbers are found

# Save unique numbers to CSV
def save_to_csv():
    with open('unique_numbers.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Number"])
        for number in unique_numbers:
            writer.writerow([number])
    print("Unique numbers saved to unique_numbers.csv")

# Main function to handle multithreading
def main():
    # Characters to iterate over: lowercase letters, numbers, and some special characters
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] + \
            [str(d) for d in range(0, 10)] + \
            ['!', '@', '#', '$', '%', '&', '*', '+', '-', '_', '='] 
            
    char_pairs = [''.join(pair) for pair in itertools.product(chars[:27], repeat=2)]  # use chars[:27] to limit to a-z + 'ñ'

    full_char_list = chars + char_pairs 

    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers based on your system's capability
        futures = []
        for j in full_char_list:
            futures.append(executor.submit(fetch_data, j))

        # Ensure all threads are completed
        for future in futures:
            future.result()

    # Save results to CSV
    save_to_csv()

if __name__ == "__main__":
    main()
