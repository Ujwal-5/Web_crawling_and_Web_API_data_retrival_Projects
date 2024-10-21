---
name: DUBAI Web Crawling and Data Extraction
description: A project for extracting and analyzing data from Dubai-based sources, storing results in HTML and other formats for efficient data management and analysis.
author: UJWAL S
tags: [web crawling, data extraction, Python, automation, Dubai, HTML, monitoring, ONNX]
---

# DUBAI Web Crawling and Data Extraction

## Overview
The DUBAI Web Crawling and Data Extraction project automates the process of gathering data from Dubai-based websites. It uses Python scripts for data extraction and monitoring, storing the results in HTML format and CSV for easy analysis and further processing.

## Table of Contents
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)

## Project Structure

    DUBAI:
    │   configs.yaml
    │   model.onnx
    │   screenshot.png
    │   XSAENER_10871559_MASTER-SERVICES-L-L-C.html
    │   XSAENER_10874415_ARTIA-JEWELLERY-L-L-C.html
    │   XSAENER_10875161_AL-ARSHAD-TECHNICAL-SERVICES-L-L-C.html
    │   XSAENER_10875194_A-M-G-CONTRACTING-L-L-C.html
    │   xsaener_crawling_15.py
    │   xsaener_moniter.json
    │   xsaener_moniter.py
    │
    └───CBLS_number_based_crawling
        │   configs.yaml
        │   model.onnx
        │   numbers_checked.csv
        │   numbers_to_check.csv
        │   screenshot.png
        │   start_crawler.bat
        │   successfully_crawled.csv
        │   test.ipynb
        │   XSAENER_10868873_SALES-PRO-GENERAL-TRADING-LLC.html
        │   XSAENER_10868900_T-M-C-SERVICES-L-L-C-.html
        │   XSAENER_10868939_I-T-WORKS-SOLUTIONS-L-L-C.html
        │   XSAENER_10869039_F-F-A-GENERAL-TRADING-L-L-C.html
        │   XSAENER_10869053_A-L-M-AUTO-SPARE-PARTS-TRADING-L-L-C.html
        │   XSAENER_10870486_ALI-AMAR-GEMS-AND-JEWELLERY-L-L-C.html
        │   XSAENER_10871398_M-V-P-APPLIANCES-L-L-C.html
        │   XSAENER_10874415_ARTIA-JEWELLERY-L-L-C.html
        │   XSAENER_10875161_AL-ARSHAD-TECHNICAL-SERVICES-L-L-C.html
        │   XSAENER_10875194_A-M-G-CONTRACTING-L-L-C.html
        │   xsaener_crawling_17.py
        │   xsaener_licence_no_crawling.py
        │   xsaener_moniter.json
        │   xsaener_moniter.py
        │
        ├───html
        │       XSAENER_240754_-.html
        │       XSAENER_240754_ARABUILD-L-L-C-.html
        │       XSAENER_511128_-.html
        │       XSAENER_511128_HAMDA-ALI-A-C-REPAIRING.html
        │       XSAENER_529321_A.html
        │       XSAENER_535793_AL-NASSER-DUBAI.html
        │       XSAENER_535793_AL-YAMAMA-PHARMACY-LLC.html
        │       XSAENER_567331_ONE-MOBILE-BR-OF-AXIOM-TELECOM-LLC-SHJ-BR-.html
        │       XSAENER_583247_-.html
        │       XSAENER_724910_AL-MOTAWEF-GENERAL-TRADING-L-L-C.html
        │
        └───__pycache__
                xsaener_moniter.cpython-310.pyc

## Key Features
- **Web Crawling:**
  - `xsaener_crawling_15.py` and `xsaener_crawling_17.py` automate data extraction from Dubai-based websites.
  - Extracted data is stored in HTML format for structured review and analysis.
  - Supports crawling based on various criteria like CBLS numbers and license numbers.

- **Data Storage:**
  - **HTML Files:** Store the structured extracted data.
  - **CSV Files:** Logs of processed and unprocessed numbers.

- **Monitoring and Automation:**
  - `xsaener_moniter.py` enables monitoring of the crawling process.
  - Integration with scheduling tools like `cron` or Windows Task Scheduler for regular data extraction and updates.

- **Model Integration:**
  - Uses an ONNX model for data predictions or processing as part of the extraction process.

## Technologies Used
- **Programming Languages:** Python, PHP  
- **Libraries & Frameworks:**
  - `requests`, `beautifulsoup4` for web crawling and parsing HTML content.
  - `onnxruntime` for utilizing the ONNX model in data processing.
  - Jupyter Notebook for data analysis and testing.

## Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/DUBAI.git
   cd DUBAI

## Usage Guide
 - Run the Web Crawler:

    python xsaener_crawling_15.py

 - For number-based crawling, use:
    
    python CBLS_number_based_crawling/xsaener_crawling_17.py

## Configuration
 - Adjust Target URLs: Modify the URLs and extraction logic within xsaener_crawling_15.py and xsaener_crawling_17.py to customize the data sources.
 - Output Settings: Change the output path for HTML and CSV files as needed directly in the scripts or through command-line arguments.
 - ONNX Model: Update the model path in configs.yaml if using a different model for predictions.