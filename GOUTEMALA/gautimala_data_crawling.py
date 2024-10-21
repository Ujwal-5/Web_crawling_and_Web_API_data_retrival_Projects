import requests
import csv
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define the API URL template
url_template = "https://svc.c.sat.gob.gt/api/sat_rtu/contribuyentes/datos/general/constancia/publica/{nit}"

# Headers with authorization
headers = {
    'accept': 'application/json',
    'authorization': 'Bearer crLh9ziUzgCVIIdcifo5vcGseOZG3zlRsRsqwr2eIss.Dbc82subT_BopSZJ8bJPaxw-izf09rvwSM4Nu9QAsA4'
}

# Function to make an API request for a given NIT
def fetch_nit_data(nit):
    try:
        # Format the URL with the NIT number
        url = url_template.format(nit=nit)
        # print(url)
        response = requests.get(url, headers=headers)

        # Check if the response is successful
        if response.status_code == 200 and nit in str(response.json()):
            save_to_json(response.json(), f'{nit}.json')
            return {nit: True}  # Return NIT as key and JSON data
        else:
            print(f"Failed to fetch data for NIT: {nit}, Status Code: {response.status_code}")
            return {nit: None}
    except Exception as e:
        print(f"Error fetching data for NIT {nit}: {e}")
        return {nit: None}

# Function to save the data as JSON
def save_to_json(data, filename):
    output_dir = 'nit_data'  # Define the output directory
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Data saved to {filepath}")

# Function to process NITs from CSV and use multithreading
def process_nits_from_csv(csv_file):
    nit_list = []
    
    # Read the CSV file to get NIT numbers
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            nit_list.append(row[0])  # Assuming each row has one NIT per line

    results = []
    print("nit_list is complete")
    # Use ThreadPoolExecutor to handle API requests concurrently
    with ThreadPoolExecutor(max_workers=1000) as executor:  # Adjust max_workers as needed
        futures = {executor.submit(fetch_nit_data, nit): nit for nit in nit_list}

        # Collect the results as each thread completes
        for future in as_completed(futures):
            nit = futures[future]
            try:
                data = future.result()
                if data:
                    results.append(data)
            except Exception as e:
                print(f"Error processing NIT {nit}: {e}")

    # Save the results to a JSON file
    save_to_json(results, 'nit_results.json')

# Example usage: Specify the CSV file containing NIT numbers
csv_file = r"C:\Scripts\GOUTIMALA\crawled_nif_list.csv"
process_nits_from_csv(csv_file)
