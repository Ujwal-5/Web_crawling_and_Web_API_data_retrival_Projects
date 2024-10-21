---
name: PANAMA Web Crawling Project
description: A project for automated data extraction from Panamanian websites, featuring Recaptcha bypass and structured data storage.
author: UJWAL S
tags: [web crawling, data extraction, Python, Recaptcha bypass, automation, Panama]
---

# PANAMA Web Crawling Project

## Overview
The PANAMA Web Crawling Project automates data extraction from Panamanian websites. It includes mechanisms for bypassing Google Recaptcha challenges and storing extracted data in HTML format. The project is designed to ensure smooth and efficient crawling processes with automated monitoring.

## Table of Contents
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)

## Project Structure

    PANAMA:
    │   .env
    │   database.py
    │   driver_config.py
    │   folder.py
    │   moniter.py
    │   panama_moniter.json
    │   panam_crawling.py
    │   RecaptchaSolver.py
    │   s3_move.py
    │   settings.py
    │   start_crawler.bat
    │
    ├───GoogleRecaptchaBypass-main
    │   │   .gitattributes
    │   │   .gitignore
    │   │   README.md
    │   │   RecaptchaSolver.py
    │   │   requirements.txt
    │   │   test.py
    │   │
    │   ├───docs
    │   │       capsolver.jpg
    │   │       demo.gif
    │   │
    │   └───__pycache__
    │           RecaptchaSolver.cpython-310.pyc
    │
    └───html
            155623365_155623365-2-2016.html
            155631621_155631621-2-2016.html
            155631622_155631622-2-2016.html
            155631623_155631623-2-2016.html
            155631624_155631624-2-2016.html
            155631625_155631625-2-2016.html


## Key Features
- **Automated Data Extraction:**
  - `panam_crawling.py` extracts data from Panamanian websites and saves it as HTML files.
  - Uses `database.py` for interacting with databases to store and retrieve information.

- **Recaptcha Bypass:**
  - `RecaptchaSolver.py` in collaboration with the `GoogleRecaptchaBypass-main` module handles Recaptcha challenges, ensuring uninterrupted data extraction.

- **Data Storage:**
  - Extracted data is organized and saved in the `html` folder for easy access and manual review.
  - `s3_move.py` enables data transfer to Amazon S3 for secure storage.

- **Process Monitoring:**
  - `moniter.py` tracks the progress and status of the crawling process, logging results in `panama_moniter.json`.

## Technologies Used
- **Programming Language:** Python
- **Libraries & Frameworks:**
  - Selenium for web crawling
  - Requests and BeautifulSoup for HTML parsing
  - Custom Recaptcha solving logic
- **Tools:** Amazon S3 for data storage, HTML for output

## Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/PANAMA.git
   cd PANAMA

## Usage Guide
 - Start the Crawling Process: Use the provided batch file to initiate the crawling:-

    start_crawler.bat

 - This will trigger panam_crawling.py and start data extraction.
 - Bypass Recaptcha Challenges:The Recaptcha solver will automatically handle challenges during crawling.

 - Monitor progress in panama_moniter.json for any issues.
 - Move Data to S3: after crawling, run

    python s3_move.py

## Configuration
- Crawler Settings: Adjust target URLs and parsing rules in panam_crawling.py to match the structure of the website.
 - Recaptcha Solver: Fine-tune settings in RecaptchaSolver.py and GoogleRecaptchaBypass-main/requirements.txt for optimal performance.
 - Environment Variables: Define keys and secrets in .env to securely access required resources.