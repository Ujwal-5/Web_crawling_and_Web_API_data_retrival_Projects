---
name: ONTARIO Web Crawling and Data Extraction
description: A project for extracting and analyzing data from Ontario sources, storing results in JSON format and HTML files for efficient data management and analysis.
author: UJWAL S
tags: [web crawling, data extraction, Python, PHP, automation, Ontario, JSON, HTML]
---

# ONTARIO Web Crawling and Data Extraction

## Overview
The ONTARIO Web Crawling and Data Extraction project automates the process of gathering data from Ontario-based websites. It uses a combination of Python and PHP scripts for data extraction, storing the results in JSON and HTML formats for easy analysis and further processing.

## Table of Contents
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)

## Project Structure

    ONTARIO:
    │   abc2.html
    │   Browser_ON.class.php
    │   ca_final2_new_v2.php
    │   ontario.json
    │   ontario_cookie_extraction.py
    │   start_crawler.bat
    │
    └───html


## Key Features
- **Web Crawling:**
  - `ontario_cookie_extraction.py` automates cookie extraction, enabling authenticated data access.
  - `ca_final2_new_v2.php` and `Browser_ON.class.php` facilitate data extraction using PHP, handling complex data scraping requirements.
  - Captures and stores extracted data in JSON format for structured analysis.

- **Data Storage:**
  - **JSON File:** `ontario.json` stores the extracted data, allowing for easy data manipulation and integration with analysis tools.
  - **HTML Files:** `abc2.html` and other files in the `html` folder provide raw data views, useful for validation and manual inspection.

- **Automation:**
  - The project includes `start_crawler.bat` for quickly initiating the data extraction process.

## Technologies Used
- **Programming Languages:** Python, PHP  
- **Libraries & Frameworks:**
  - `requests`, `beautifulsoup4` for Python-based web crawling.
  - PHP for handling web interactions and advanced scraping tasks.
  - `json` for structured data storage.

## Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/ONTARIO.git
   cd ONTARIO

## Usage Guide
 - Run the Web Crawler:

   start_crawler.bat

## Configuration
 - Adjust Target URLs: Modify the URLs and extraction logic within ca_final2_new_v2.php and Browser_ON.class.php to customize the data sources.
 - Output Settings: Update paths for output JSON files and HTML files directly in the scripts.