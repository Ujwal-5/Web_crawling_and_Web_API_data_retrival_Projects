
---
name: SAUDI_ARABIA Web Crawling Project
description: A project for automated data extraction from Saudi Arabian websites, with results stored in HTML and JSON formats.
author: UJWAL S
tags: [web crawling, data extraction, Python, automation, Saudi Arabia, JSON, HTML]
---

# SAUDI_ARABIA Web Crawling Project

## Overview
The SAUDI_ARABIA Web Crawling Project automates the process of extracting data from Saudi Arabian websites. The extracted data is stored in JSON and HTML formats, providing structured storage for further analysis or integration.

## Table of Contents
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)

## Project Structure

    SOUDI_ARABIA:.
    │   Cawling_by_CRName.py
    │   crawling_by_pegination.py
    │   foo.png
    │   model.onnx
    │   saudi.json
    │
    └───html2
            3350152742.html
            4032002163.html
            4032002292.html
            4032002468.html
            4032002515.html
            4032002525.html
            4032002532.html
            4032002548.html
            4032002662.html
            4032002675.html
            4032002913.html


## Key Features
- **Automated Data Extraction:**
  - `Cawling_by_CRName.py` extracts data based on commercial registration names.
  - `crawling_by_pegination.py` handles data extraction from paginated websites.
  
- **Machine Learning Integration:**
  - The `model.onnx` file suggests a possible machine learning model for tasks like solving captchas or text extraction.

- **Data Storage:**
  - Extracted data is stored in `saudi.json` for structured access.
  - Raw HTML responses are saved in the `html2` folder for further parsing or debugging.

## Technologies Used
- **Programming Language:** Python
- **Libraries & Frameworks:** 
  - Requests or Selenium for web scraping
  - ONNX for machine learning model inference
  - JSON for structured data storage

## Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/SAUDI_ARABIA.git
   cd SAUDI_ARABIA

## Usage Guide
 - Start the Crawling Process: To extract data using commercial registration names
    
    python Cawling_by_CRName.py

 - To perform paginated crawling:
    
    python crawling_by_pegination.py

## Configuration
 - Crawling Settings: Adjust target URLs and parsing rules within the Python scripts to match the structure of the websites.
 - Model Integration: If using model.onnx, ensure it is properly referenced in the scripts for any machine learning tasks.
- Output Location: By default, extracted data is saved in saudi.json and html2 folder. You can change this within the scripts if needed.