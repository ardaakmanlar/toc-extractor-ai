# toc-extractor-ai

A tool that extracts Table of Contents from book screenshots using the Gemini API.

---

## About the Project

This project was developed during my internship at **FERNUS**, an educational technology company.

FERNUS Studio lacked a tool for extracting Tables of Contents (ToC) from book screenshots.  
This project was created to automate that task using AI, replacing manual and repetitive methods.

It was specifically built for internal use at FERNUS to support the content preparation process and reduce the manual workload involved in book production.

---

## Features

- Extracts Table of Contents from book images
- Uses Gemini API to perform AI-based extraction
- Applies image preprocessing for better consistency
- Allows exporting results as Excel (`.xlsx`) or plain text (`.txt`)
- Includes model selection to switch between Gemini model versions
- Supports both Turkish and English user interfaces
- Displays detailed logs to assist with debugging and tracking

---

## Tech Stack

- Python
- Gemini API
- OpenCV – image preprocessing
- pandas - data handling 
- openpyxl –  excel export
- tkinter – desktop GUI

---

## User Interface Overview

![Screenshot of the application](https://github.com/user-attachments/assets/57ec53e4-d748-4f8e-a512-3997302909fc)

- **Load Images**: Select screenshots to process  
- **Save as Excel / TXT**: Export the extracted table of contents  
- **Model Selector**: Choose the Gemini model to use  
- **View Log**: Display process details and backend responses  
- **Türkçe**: Switch interface language to Turkish
