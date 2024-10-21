<!-- ⚠️ This README has been generated from the file(s) "blueprint.md" ⚠️-->---
name: GUATEMALA Web Crawling and Data Extraction
description: A project for extracting and analyzing data from Guatemala sources, storing results in JSON format for efficient data management and analysis.
author: UJWAL S
tags: [web crawling, data extraction, Python, automation, Guatemala, JSON, CSV]
---


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#guatemala-web-crawling-and-data-extraction)

# ➤ GUATEMALA Web Crawling and Data Extraction


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#overview)

## ➤ Overview
The GUATEMALA Web Crawling and Data Extraction project automates the process of gathering data from websites based in Guatemala. It uses Python scripts for data extraction, storing the results in JSON and CSV formats for easy analysis and further processing.


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

    GOUTEMALA:.
    │   crawled_nit_list.csv
    │   gautimala_nit_crawling.py
    │   gautimala_data_crawling.py
    │   output_image.png
    │   
    └───nit_data
            10758.json
            13757.json
            14079.json
            30740.json
            31615.json
            32018.json
            32913.json
            34525.json
            34533.json
            36978.json
            39497.json
            42366.json
            62294.json
            64424.json
            66850.json



[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#key-features)

## ➤ Key Features
- **Web Crawling:**
  - `gautimala_nit_crawling.py` automates the nit numbers extraction process from Guatemala-based websites.
  - `gautimala_data_crawling.py` is used for specific data crawling tasks.
  - Supports data storage in JSON format for structured analysis.

- **Data Storage:**
  - **JSON Files:** Store structured data for each NIT (Tax Identification Number).
  - **CSV Files:** `crawled_nit_list.csv` logs all the processed NITs for easy tracking and updates.

- **Visualization:**
  - `output_image.png` provides a sample view of the extracted data or visual representation of the data crawling process.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#technologies-used)

## ➤ Technologies Used
- **Programming Languages:** Python  
- **Libraries & Frameworks:**
  - `requests`, `beautifulsoup4` for web crawling and parsing HTML content.
  - `json` for structured data storage.
  - `pandas` for handling CSV files and data analysis.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#setup-instructions)

## ➤ Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/GUATEMALA.git
   cd GUATEMALA


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#usage-guide)

## ➤ Usage Guide
 - Run the Web Crawler: