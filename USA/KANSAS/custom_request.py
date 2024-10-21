import time
from requests import RequestException
import random
import cloudscraper

def make_request_with_retry(url, session, method, headers, data, max_retries, retry_delay):
    for attempt in range(max_retries):
        scraper = cloudscraper.create_scraper()
        time.sleep(random.uniform(1,5))
        try:
            if method == 'post' or method == 'POST':
                response = scraper.post(url,headers=headers, data=data)
                response.raise_for_status()  # Raise an error for non-2xx status codes
                return response
            elif method == 'get' or method == 'GET':
                response = scraper.get(url,headers=headers, data=data)
                response.raise_for_status()  # Raise an error for non-2xx status codes
                return response
        except RequestException as e:
            print(f"Request failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries exceeded. Request failed.")
                raise