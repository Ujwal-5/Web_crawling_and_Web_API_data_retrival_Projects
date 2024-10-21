import requests
from lxml import html
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import traceback
matricula_dict = {}

# Function to fetch data for each combination
def fetch_data(i):
    local_dict = []  # Local dictionary to store data for each 'k'
    
    for j in range(1,10):
        for k in ['FG']:
            try:
                print(f"Buscando matrícula {k}-{j}-{i}") 
                url = "https://sure.sinap.hn/consultas/registromercantil/publicListadoEmpresas.jsp"

                payload = f'buscoPor=porMatricula&origen=publicConsEmpresa.jsp&origenNames=destino&origenValues=publicEmpresa.jsp&destino=publicEmpresa.jsp&row={i}1&CR={k}&numEmpresa={j}&idxEmpresa=&tipoBusqueda=COMIENZACON'
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
                try:
                    response = requests.post(url, headers=headers, data=payload)
                except:
                    print("error occured")
                    continue

                html_content = html.fromstring(response.content)

                # Extract registration numbers using regex
                matricula = html_content.xpath("//a[contains(., '| Matrícula:')]/text()")
                numbers = [re.search(r'(\d+ - 00000)', item).group(0) for item in matricula if re.search(r'(\d+ - 00000)', item)]
                # print(numbers)
                if numbers:
                    # print(numbers)
                    local_dict.extend(numbers)  # Collect numbers in local_dict
                else:
                    print('No numbers found')
                    # break  # Exit loop if no numbers are found
            except:
                try:
                    traceback.print_exc()
                except:
                    pass
                continue

    return k,i, local_dict  # Return 'k' and its corresponding numbers

# Function to save numbers to a CSV file
def save_to_csv(data):
    with open('matricula_numbers.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Key', 'Number'])
        for key, numbers in data.items():
            for number in numbers:
                writer.writerow([key, number])
    print("Numbers saved to matricula_numbers.csv")

# Main function to execute multithreading
def main():
    #'FG', 'HC'
    keys = ['FG', 'HC']#['AA', 'AB', 'CD', 'DE', 'DF', 'EF', 'GI', 'GJ', 'BK', 'IL', 'JM', 'KN', 'LO', 'LP', 'MO', 'NR', 'OS', 'PT', 'RW', 'RX', 'RY', 'WU', 'WV', ''FH']
    
    with ThreadPoolExecutor(max_workers=100) as executor:  # Adjust max_workers based on your system
        futures = {executor.submit(fetch_data, i): i for i in range(5800)}

        # Collect results as they complete
        for future in as_completed(futures):
            k,i, numbers = future.result()
            if numbers:
                if k in matricula_dict:
                    matricula_dict[k].extend(numbers)
                else:
                    matricula_dict[k] = numbers
            else:
                print(f"No matrícula found for key {i}")

    # Save results to CSV
    save_to_csv(matricula_dict)

if __name__ == "__main__":
    main()
