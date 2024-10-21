import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import os

# Function to get detailed data for a specific registration number
def get_data(raw_num):
    try:
        CR, num_empresa = raw_num.split(',')
        num_empresa_trimmed = num_empresa.split(' - ')[0]
        print(num_empresa_trimmed)
        num_empresa = num_empresa.replace('-', '').strip()  # Clean up num_empresa
        url = f"https://sure.sinap.hn/consultas/registromercantil/publicEmpresa.jsp?CR={CR.strip()}&numEmpresa={num_empresa_trimmed.strip()}&idxEmpresa=00000&acceso=qlkKEZz%2Bt2aN%2F2cEYkd1tR0x8LGwDdgB#"
        # print(url)

        response = requests.get(url, timeout=10)  # Adding timeout to handle slow responses

        if response.status_code == 200 and num_empresa_trimmed.strip() in response.text:
            print('Success')
            try:
                # Save the HTML content to a file
                os.makedirs("html", exist_ok=True)
                with open(f"html/{num_empresa_trimmed.strip()}.html", "w", encoding="utf-8") as f:
                    f.write(response.text)
            except Exception as e:
                print(f"Error saving HTML for {num_empresa_trimmed.strip()}: {e}")
            return "Success"
        else:
            print("Failure")
            return "Failure"

    except requests.exceptions.RequestException as e:
        print(f"Network error for {raw_num}: {e}")
        return "Network Error"
    except ValueError as e:
        print(f"Error processing {raw_num}: {e}")
        return "Processing Error"
    except Exception as e:
        print(f"Unexpected error for {raw_num}: {e}")
        return "Unexpected Error"

def main():
    input_file = "C:\\Scripts\\hondurus\\matricula.csv"
    output_file = "C:\\Scripts\\hondurus\\matricula_numbers_updated_retry.csv"

    try:
        # Read data from the CSV
        with open(input_file, "r") as file:
            reader = csv.DictReader(file)
            data = list(reader)
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
        return
    except Exception as e:
        print(f"Error reading the file {input_file}: {e}")
        return

    # Add 'Status' column if it doesn't exist
    if 'Status' not in reader.fieldnames:
        fieldnames = reader.fieldnames + ['Status']
    else:
        fieldnames = reader.fieldnames

    # Prepare the data for processing
    cleaned_data = [f"{row['Key']},{row['Number']}" for row in data]

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(get_data, num): num for num in cleaned_data}

        # Update each row with the corresponding status
        for future in as_completed(futures):
            num = futures[future]
            try:
                result = future.result()
            except Exception as e:
                print(f"Error processing {num}: {e}")
                result = "Error"

            # Find the matching row and update its status
            key, number = num.split(',')
            for row in data:
                if row['Key'] == key and row['Number'] == number:
                    row['Status'] = result

    try:
        # Write the updated data to a new CSV
        with open(output_file, "w", newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print("Updated CSV saved successfully.")
    except Exception as e:
        print(f"Error writing the updated CSV file: {e}")

if __name__ == "__main__":
    main()
