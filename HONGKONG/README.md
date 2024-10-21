<!-- ⚠️ This README has been generated from the file(s) "blueprint.md" ⚠️-->---
name: HONGKONG Web Crawling and Data Retrieval
description: A project for extracting and managing data from Hong Kong business registries and ICRIS, focusing on BRN data crawling and purchasing system automation.
author: UJWAL S
tags: [web crawling, data extraction, Python, automation, Hong Kong, BRN, ICRIS]
---


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#hongkong-web-crawling-and-data-retrieval)

# ➤ HONGKONG Web Crawling and Data Retrieval


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#overview)

## ➤ Overview
The HONGKONG Web Crawling and Data Retrieval project focuses on automating data extraction from the Hong Kong Business Registry and managing purchases on the ICRIS platform. It includes Python scripts for BRN data crawling and purchasing system automation using the ICRIS platform.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#table-of-contents)

## ➤ Table of Contents
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#project-structure)

## ➤ Project Structure
    
    HONGKONG:.
    ├───HKBRN_data_crawling
    │       brn_data_crawling.py
    │
    └───icris_purchasing
            database.py
            driver_config.py
            enter_captcha.py
            folder.py
            new_purchase.py
            settings.py
            xsicris_order.py



[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#key-features)

## ➤ Key Features
- **BRN Data Crawling:**
  - `brn_data_crawling.py` automates the extraction of Business Registration Numbers (BRN) from relevant sources in Hong Kong.
  - Captures and stores data for further analysis and business use cases.

- **ICRIS Purchasing Automation:**
  - `new_purchase.py` automates the purchasing of business data from the ICRIS platform.
  - **Captcha Handling:** `enter_captcha.py` automates the handling of captchas during the purchasing process.
  - **Driver Configuration:** `driver_config.py` manages web drivers for browser automation.
  - **Database Interaction:** `database.py` supports data persistence and order management.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#technologies-used)

## ➤ Technologies Used
- **Programming Languages:** Python
- **Libraries & Frameworks:**
  - `selenium` for web automation and crawling.
  - `requests`, `beautifulsoup4` for web scraping and parsing HTML content.
  - `pandas` for handling structured data.
  - `sqlite3` for database management.
- **Tools:** Web drivers (e.g., ChromeDriver) for browser automation.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#setup-instructions)

## ➤ Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/HONGKONG.git
   cd HONGKONG


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#usage-guide)

## ➤ Usage Guide
 - BRN Data Crawling:
 - Run the BRN data extraction script:
    
    python HKBRN_data_crawling/brn_data_crawling.py

### ICRIS Purchasing Automation:
 - To automate the purchase of data from ICRIS:

    python icris_purchasing/new_purchase.py

### Captcha Handling:
 - Captchas are automatically handled by the enter_captcha.py script during the purchasing process.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#configuration)

## ➤ Configuration
 - Modify Settings: Update settings.py to configure the purchasing process, such as credentials and preferred purchase options.
 - Driver Configuration: Ensure driver_config.py has the correct web driver paths.
 - Database Settings: Configure database connections in database.py as needed for storing purchase data.