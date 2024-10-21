<!-- ⚠️ This README has been generated from the file(s) "blueprint.md" ⚠️-->---
name: NICARAGUA Web Crawling Project
description: A project for automated data extraction from Nicaraguan websites, storing outputs in JSON format and supporting data migration to S3.
author: UJWAL S
tags: [web crawling, data extraction, Python, automation, Nicaragua, JSON, S3]
---


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#nicaragua-web-crawling-project)

# ➤ NICARAGUA Web Crawling Project


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#overview)

## ➤ Overview
The NICARAGUA Web Crawling Project focuses on automating data extraction from Nicaraguan websites, saving the output in JSON format, and providing a mechanism to transfer the data to AWS S3 for further processing and storage.


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

    NICARAGUA:.
    │   move_to_s3.bat
    │   NICARAGUA_crawling.py
    │
    ├───JSON
    └───KEYWORD_JSON
            aa.json
            ab.json
            ac.json
            ae.json
            af.json
            ag.json
            ah.json
            ai.json
            aj.json
            ak.json
            am.json
            ao.json



[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#key-features)

## ➤ Key Features
- **Automated Data Extraction:**
  - `NICARAGUA_crawling.py` script performs web crawling and extracts data from Nicaraguan websites.
  - Extracted data is stored in JSON format, making it easy to process and analyze.

- **Batch Data Transfer:**
  - `move_to_s3.bat` facilitates the transfer of extracted data from the local JSON directories to AWS S3 for cloud storage and further processing.

- **Organized Data Storage:**
  - Data is categorized and saved in `JSON` and `KEYWORD_JSON` directories, allowing for efficient storage and retrieval based on different criteria.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#technologies-used)

## ➤ Technologies Used
- **Programming Language:** Python
- **Libraries & Frameworks:**
  - `requests`, `beautifulsoup4` for HTTP requests and HTML parsing.
  - `boto3` for interacting with AWS S3.
- **Tools:** Batch script for automating data transfers.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#setup-instructions)

## ➤ Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/NICARAGUA.git
   cd NICARAGUA


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#usage-guide)

## ➤ Usage Guide
 - Start the Crawling Process:
 - Run the data extraction script to start the crawling process:

    python NICARAGUA_crawling.py

 - Transfer Data to S3: Use the provided batch script to move JSON data to your S3 bucket

    move_to_s3.bat

 - View Extracted Data:Extracted JSON data will be stored in the JSON and KEYWORD_JSON directories for easy access and further analysis.


[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#configuration)

## ➤ Configuration
 - AWS S3 Bucket: Modify move_to_s3.bat with your specific S3 bucket details for smooth data transfers.
 - Crawler Settings: Adjust the URLs and parsing logic directly in NICARAGUA_crawling.py as per your data source requirements.
 - Output Directories: If needed, change the output paths in the script to store JSON data in custom directories.