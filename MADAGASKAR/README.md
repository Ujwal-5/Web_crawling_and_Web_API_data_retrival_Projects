<!-- ⚠️ This README has been generated from the file(s) "blueprint.md" ⚠️-->---
name: MADAGASKAR Web Crawling Project
description: A project for extracting and processing RCS data from Madagascan websites, with outputs in HTML format.
author: UJWAL S
tags: [web crawling, data extraction, Python, automation, Madagascar, RCS data]
---


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#madagaskar-web-crawling-project)

# ➤ MADAGASKAR Web Crawling Project


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#overview)

## ➤ Overview
The MADAGASKAR Web Crawling Project is designed to automate the extraction of RCS (Registre de Commerce et des Sociétés) data from Madagascan websites. It processes the data and stores the output in HTML format for further analysis.


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

    MADAGASKAR:.
    │   MG_crawling.py
    │
    └───out
            .html
            RCS Ambositra 2021 A 00051.html
            RCS Ambositra 2021 A 00059.html
            RCS Ambositra 2021 A 00064.html
            RCS Ambositra 2021 A 00067.html
            RCS Ambositra 2021 A 00071.html
            RCS Ambositra 2022 A 00008.html
            RCS Ambositra 2022 A 00012.html
            RCS Ambositra 2022 A 00019.html
            RCS Ambositra 2022 A 00020.html



[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#key-features)

## ➤ Key Features
- **Automated RCS Data Crawling:**
  - `MG_crawling.py` handles the extraction of RCS data from specified Madagascan sources.
  - Extracted data is saved in HTML files for easy viewing and further processing.

- **Structured Output:**
  - The extracted HTML files are stored in the `out/` directory, organized by their respective RCS identifiers for better manageability.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#technologies-used)

## ➤ Technologies Used
- **Programming Language:** Python
- **Libraries & Frameworks:**
  - `requests`, `beautifulsoup4` for HTTP requests and HTML parsing.
  - `selenium` for handling dynamic content if needed.
- **Tools:** Web drivers (e.g., ChromeDriver) for browser automation (if required).


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#setup-instructions)

## ➤ Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/MADAGASKAR.git
   cd MADAGASKAR


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#usage-guide)

## ➤ Usage Guide
 - Run the Crawler:
 - Execute the main script to start the data extraction process:

    python MG_crawling.py

- View Extracted Data:
 - Extracted data will be saved as HTML files in the out/ directory.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#configuration)

## ➤ Configuration
 - Modify Target URLs: Update the URLs or parameters within MG_crawling.py to adjust the target websites or RCS identifiers.
 - Output Directory: Change the output path in the script if a different storage location for HTML files is needed.