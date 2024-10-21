<!-- ⚠️ This README has been generated from the file(s) "blueprint.md" ⚠️-->---
name: INDIA Web Crawling and Data Retrieval
description: A project for extracting data from EPFO and MSME databanks in India, including automated data crawling, HTML parsing, and financial data extraction.
author: UJWAL S
tags: [web crawling, data extraction, Python, automation, India, EPFO, MSME]
---


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#india-web-crawling-and-data-retrieval)

# ➤ INDIA Web Crawling and Data Retrieval


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#overview)

## ➤ Overview
The INDIA Web Crawling and Data Retrieval project focuses on extracting and managing data from Indian websites, including EPFO (Employee Provident Fund Organization) codes and MSME (Micro, Small & Medium Enterprises) databank information. The project involves crawling data, parsing HTML, handling captchas, and managing configurations for automated data extraction.


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

    INDIA:.
    ├───EPFO_SITE
    │   │   configs.yaml
    │   │   epfo_code_extraction.py
    │   │   epfo_code_extraction.spec
    │   │   epfo_code_extraction_2.py
    │   │   model.onnx
    │   │   xsinepfo.json
    │   │   xsinepfo_crawling.ipynb
    │   │   xsinepfo_crawling.py
    │   │
    │   ├───html
    │   │       APHYD0006233000.html
    │   │       APHYD0018542000.html
    │   │       APHYD0018662000.html
    │   │       APHYD0019987000.html
    │   │       APHYD0031065000.html
    │   │       APHYD0031529000.html
    │   │       APHYD0032426000.html
    │   │       APHYD0034963000.html
    │   │       APHYD0052112000.html
    │   │
    │   └───html_financial
    │           APHYD0014252000.html
    │           APHYD0018627000.html
    │           APHYD0029081000.html
    │           APHYD0041944000.html
    │           APHYD0044147000.html
    │           APHYD0052069000.html
    │           APHYD0056181000.html
    │           APHYD0056984000.html
    │           APHYD0061090000.html
    │           APHYD0061331000.html
    │           APHYD0061408000.html
    │           APHYD0063828000.html
    │           APHYD0064836000.html
    │           APHYD0072150000.html
    │           APHYD0073292000.html
    │           APHYD0073366000.html
    │
    └───MSME_DATABANK
            captcha.png
            MSME_databank_crawling.ipynb
            MSME_databank_crawling.py
            result.html



[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#key-features)

## ➤ Key Features
- **EPFO Data Crawling:**
  - Scripts and notebooks (`epfo_code_extraction.py`, `xsinepfo_crawling.py`) automate the extraction of EPFO codes and associated data.
  - Handles different HTML structures to capture both general and financial data, storing results in structured formats.

- **MSME Databank Crawling:**
  - `MSME_databank_crawling.py` automates the extraction of information from the MSME databank.
  - Includes a method for solving captcha challenges using image recognition.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#technologies-used)

## ➤ Technologies Used
- **Programming Languages:** Python
- **Libraries & Frameworks:**
  - `selenium` for web automation.
  - `requests`, `beautifulsoup4` for web scraping and HTML parsing.
  - `onnxruntime` for loading and running the ONNX model.
  - `pandas` for data handling and storage.
- **Tools:** PyInstaller for creating executable versions of the scripts, Web drivers (e.g., ChromeDriver) for browser automation.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#setup-instructions)

## ➤ Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/INDIA.git
   cd INDIA


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#usage-guide)

## ➤ Usage Guide
 - EPFO Data Crawling:
 - Run the EPFO data extraction script:

    python EPFO_SITE/xsinepfo_crawling.py

 - MSME Databank Crawling:

 - To extract MSME databank information, run:

    python MSME_DATABANK/MSME_databank_crawling.py


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#configuration)

## ➤ Configuration
 - Modify Settings: Update configs.yaml in the EPFO_SITE folder to configure crawling settings, such as URLs and parameters.
 - Driver Configuration: Ensure the path to the web driver is correctly set in the Python scripts.
 - ONNX Model: The model.onnx is used for specific automation tasks—ensure it is correctly referenced in the scripts.