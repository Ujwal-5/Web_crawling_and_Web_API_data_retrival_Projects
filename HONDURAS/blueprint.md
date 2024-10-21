---
name: HONDURAS Web Crawling and Data Extraction
description: A project for extracting and analyzing data from Honduras sources, storing results in JSON format for efficient data management and analysis.
author: UJWAL S
tags: [web crawling, data extraction, Python, automation, Honduras, JSON, HTML, PHP]
---

# HONDURAS Web Crawling and Data Extraction

## Overview
The HONDURAS Web Crawling and Data Extraction project automates the process of gathering data from websites based in Honduras. It includes Python scripts for data extraction and conversion of HTML data into JSON format, storing the results for easy analysis and further processing.

## Table of Contents
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)

## Project Structure

    HONDURAS:.
    │   hondurs_crawling.py
    │   html_encoding_fix.py
    │   matricula_numbers.csv
    │   matricula_numbers_crawling.py
    │
    ├───html
    └───HTML_TO_JSON
        │   html_2_json.php
        │
        └───county
            ├───done
            │       0000000025.html
            │       0000000026.html
            │       0000000027.html
            │       0000000028.html
            │
            ├───html
            │       0000007857.html
            │       0000007858.html
            │       0000007859.html
            │       0000007860.html
            │       0000007861.html
            │       0000007862.html
            │       0000007863.html
            │       0000007864.html
            │       0000007865.html
            │       0000007866.html
            │       0000007867.html
            │       0000007868.html
            │       0000007869.html
            │       0000007870.html
            │
            ├───json
            │       0000000025.json
            │       0000000026.json
            │       0000000027.json
            │       0000000028.json
            │       0000000029.json
            │       0000000030.json
            │       0000000031.json
            │       0000000032.json
            │       0000000033.json
            │
            └───skip


## Key Features
- **Web Crawling:**
  - `hondurs_crawling.py` automates data extraction from websites based in Honduras.
  - `matricula_numbers_crawling.py` focuses on extracting data using matricula numbers from `matricula_numbers.csv`.

- **Data Conversion:**
  - `html_2_json.php` converts HTML data into JSON format for better data organization and analysis.
  - **HTML to JSON:** Converted JSON files are stored in the `json` directory.

- **Data Storage:**
  - **HTML Files:** Stored in the `html` directory and further organized in the `HTML_TO_JSON/county` subdirectories.
  - **JSON Files:** Processed data stored in JSON format for easy integration with analysis tools.

## Technologies Used
- **Programming Languages:** Python, PHP
- **Libraries & Frameworks:**
  - `requests`, `beautifulsoup4` for web crawling and parsing HTML content.
  - `json` for structured data storage.
  - `pandas` for handling CSV files.
- **Tools:** PHP for converting HTML data into JSON.

## Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/HONDURAS.git
   cd HONDURAS

## Usage Guide
 - Run the Web Crawler:
 - Start the data extraction process using:
    
    python hondurs_crawling.py

- For crawling based on matricula numbers:
    
    python matricula_numbers_crawling.py

### Convert HTML to JSON:

 - Use html_2_json.php to convert HTML files in the HTML_TO_JSON/html directory:

    php HTML_TO_JSON/html_2_json.php

## Configuration
 - Adjust Target URLs: Modify the URLs and extraction logic within hondurs_crawling.py and matricula_numbers_crawling.py to customize the data sources.
 - Output Settings: Change the output path for HTML and JSON files as needed directly in the scripts or through command-line arguments.