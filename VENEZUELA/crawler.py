import requests
import csv
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# Define a lock for thread-safe operations
lock = Lock()

# List to store the crawled data
crawled_data = []

# Function to crawl data for each unique number
def crawl_data(number):
    try:
        url = f"https://rncenlinea.snc.gob.ve/planilla/index/{number}?anafinan=N&anafinanpub=Y&login=N&mostrar=INF"  # Replace with your actual URL pattern
        response = requests.get(url)
        
        if response.status_code == 200:
            # Process the response as needed
            print(f"Successfully fetched data for number: {number}")
            with open(f"data/{number}.html", "w", encoding="utf-8") as file:
                file.write(response.text)
            return (number, response.text)  # Storing both number and content
        else:
            print(f"Failed to fetch data for number: {number} with status code {response.status_code}")
            return (number, None)
    except Exception as e:
        print(f"Error fetching data for number {number}: {e}")
        return (number, None)

# Function to read unique numbers from CSV
def read_numbers_from_csv(file_path):
    numbers = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            numbers.append(row[0])  # Assumes the number is in the first column
    return numbers

# Function to save the crawled data to a new CSV file
def save_crawled_data(crawled_data):
    with open('crawled_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Number", "Data"])  # Header row
        for number, data in crawled_data:
            writer.writerow([number, data])
    print("Crawled data saved to crawled_data.csv")

# Main function to handle multithreading
def main():
    # Read unique numbers from CSV
    numbers = read_numbers_from_csv('unique_numbers.csv')

    with ThreadPoolExecutor(max_workers=100) as executor:  # Adjust max_workers based on your system's capability
        futures = {executor.submit(crawl_data, number): number for number in numbers}

        for future in futures:
            result = future.result()
            if result[1] is not None:  # Check if data was successfully fetched
                with lock:
                    crawled_data.append(result)

    # Save all crawled data to a CSV file
    save_crawled_data(crawled_data)

if __name__ == "__main__":
    main()
