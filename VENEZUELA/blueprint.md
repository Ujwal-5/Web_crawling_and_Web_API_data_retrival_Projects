---
name: VENEZUELA Web Crawling Project
description: A project for automated data extraction from Venezuelan websites, with results stored in HTML and CSV formats.
author: UJWAL S
tags: [web crawling, data extraction, Python, automation, Venezuela, CSV, HTML]
---

# VENEZUELA Web Crawling Project

## Overview
The VENEZUELA Web Crawling Project automates the extraction of data from websites in Venezuela. The data is stored in HTML files and summarized in a CSV file, making it easy to access and analyze unique information collected from the crawling process.

## Table of Contents
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)

## Project Structure

    VENEZUELA:.
    │   crawler.py
    │   crawl_unique_numbers.py
    │   unique_numbers.csv
    │   venzuela_exp.ipynb
    │
    └───data
            12335.html
            12626.html
            14580.html
            15510.html
            15557.html
            16693.html
            17150.html
            18428.html


## Key Features
- **Automated Data Extraction:**
  - `crawler.py` is used to extract data from various websites in Venezuela.
  - The raw HTML responses are stored in the `data` folder for further reference or processing.

- **Unique Number Extraction:**
  - `crawl_unique_numbers.py` extracts unique numbers or identifiers from the crawled HTML data.
  - The results are stored in `unique_numbers.csv` for easy access and analysis.

- **Data Analysis:**
  - `venzuela_exp.ipynb` contains scripts and visualizations for analyzing the crawled data, providing insights into the collected information.

## Technologies Used
- **Programming Language:** Python
- **Libraries & Frameworks:** 
  - Requests for HTTP requests
  - BeautifulSoup for HTML parsing
  - Pandas for data manipulation and analysis
- **Tools:** Jupyter Notebook for analysis, CSV for data storage

## Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/VENEZUELA.git
   cd VENEZUELA

## Usage Guide
 - Start the Crawling Process:

    python crawler.py

 - Extract Unique Numbers:

    python crawl_unique_numbers.py

## Configuration
- Crawling Settings: Adjust target URLs, user agents, and other crawling settings within crawler.py.
 - Output Location: By default, data is saved in the data folder and unique_numbers.csv. Modify paths in the scripts if you want to change the output locations.