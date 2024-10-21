import requests
import itertools
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback

def fetch_data(keyword):
    url = f"https://ventanilla.siicar.gob.ni/VentanillaPrivada/API/VentanillaLinea/ObtenerEstadoSociedad?pTipoBusqueda=Nombre&pValorBusqueda={keyword}"
    headers = {}
    payload = {}
    
    try:
        response = requests.get(url, headers=headers, data=payload, timeout=250)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data_json = response.json()
        print(data_json)
        # Save each keyword's data to a separate JSON file
        if 'Execution Timeout Expired' not in str(data_json):
            with open(f'KEYWORD_JSON/{keyword}.json', mode='w', encoding='utf-8') as file:
                json.dump(data_json, file, ensure_ascii=False, indent=4)
                
            with open(f"KEYWORD_JSON\\{keyword}.json", mode='r', encoding='utf-8') as file:
                json_string = file.read().strip()  # Remove leading/trailing whitespace


            data = json.loads(json_string.strip())
            data2 = json.loads(data)
            for entry in data2:
                numero_unico = entry['NumeroUnico']
                # Create a filename with the NumeroUnico
                filename = f"JSON/{numero_unico}.json"
            
                # Save the entry as a JSON file
                with open(filename, 'w', encoding='utf-8') as file:
                    json.dump(entry, file, ensure_ascii=False, indent=4)
            
            print(f"Data for keyword '{keyword}' saved successfully.")
        else:
            print("no data/error", keyword)
    except Exception as e:
        print(f"Failed to fetch data for keyword '{keyword}': {e}")
        print(traceback.print_exc())

def main():
    # Generate all combinations from 'aa' to 'zz'
    combinations = ['ad','al','an','ar','ca','ci','da','el','fq','hq','ia','ic','ie','im','in','io','jq','jw','on','qf','qk','qq','qp','qx','qw','qy','qz','sx','vq','vw','wv','zd','zv']#[''.join(letters) for letters in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=2)]

    # Use ThreadPoolExecutor to handle multithreading
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_data, keyword): keyword for keyword in combinations}
        
        for future in as_completed(futures):
            keyword = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Keyword '{keyword}' generated an exception: {e}")
                print(traceback.print_exc())

if __name__ == "__main__":
    main()
