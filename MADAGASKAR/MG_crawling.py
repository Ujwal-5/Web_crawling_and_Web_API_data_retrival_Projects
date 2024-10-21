import requests
from bs4 import BeautifulSoup
import lxml.html

def scrape_website_and_save(url_template, output_directory, consecutive_fail_threshold):
    i = 1  # Initial value for i
    while True:  # Outer loop
        j = 0  # Initial value for j
        consecutive_fail_count = 0  # Counter for consecutive failed attempts
        flag = True
        while flag:  # Inner loop
            print('i = ', i)
            print('j = ', j)
            url = url_template.format(i, j)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

                # Find the table
            table = soup.find('table', class_='simple2')

                # Find the row containing the value
            row = table.find('tr')

                # Check if the row exists and then extract the value
            if row:
                cells = row.find_all('td')
                if len(cells) == 2:  # Ensure there are two cells in the row
                    value = cells[1].get_text(strip=True).replace(':', '').strip()
                    print(value)  # Output: RCS Ambositra 2000A00004
                else:
                    print("Value not found in the expected format")
            else:
                print("Table not found")
            tree = lxml.html.fromstring(response.text)

            # Evaluate the XPath expression
            Immatriculation_value = tree.xpath('//td[strong[contains(., "Immatriculation")]]/following-sibling::td/text()')
            print(f"Extracted Immatriculation_value: {Immatriculation_value[0].strip()}")

            if isinstance(value, str) and Immatriculation_value[0].strip() != ':':
                html_template = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Details</title>
                </head>
                <body>
                    <table border="1">
                        <tr>
                            <th>Range</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>i</td>
                            <td>{i}</td>
                        </tr>
                        <tr>
                            <td>j</td>
                            <td>{j}</td>
                        </tr>
                    </table>
                </body>
                </html>
                """
                full_html = html_template+response.text
                output_file = f"{output_directory}/{value}.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(full_html)
                print("HTML content saved to:", )
                # Check for the field 'Immatriculation' in the HTML content
                # soup = BeautifulSoup(response.text, 'html.parser')
                # immatriculation = soup.find('input', {'name': 'Immatriculation'})
                # if immatriculation:
                #     print("Immatriculation:", immatriculation.get('value'))
                consecutive_fail_count = 0  # Reset consecutive fail count on successful attempt
            else:
                print(f"Failed to retrieve page for parameters {i}, {j}. Status code:", response.status_code)
                consecutive_fail_count += 1
                if consecutive_fail_count >= consecutive_fail_threshold:
                    print(f"Consecutive failed attempts reached threshold for parameter {i}.")
                    flag =False  # Exit inner loop if consecutive failed attempts reached threshold
            j += 1  # Increment j
        else:
            i += 1  # Increment i if the inner loop completes without breaking
            if i > 42:
                break  # Exit outer loop if i exceeds 42
        consecutive_fail_count = 0  # Reset consecutive fail count for the next 'i'


# Example usage
url_template = "https://www.rcsmada.mg/index.php?pgdown=consultation&soc={}-{}"
output_directory = r"out"
consecutive_fail_threshold = 10

scrape_website_and_save(url_template, output_directory, consecutive_fail_threshold)

