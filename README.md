# Open-Source Excel & CSV Data Cleaner

An automated, lightweight web application built with Streamlit and Pandas to clean messy datasets, remove duplicate rows, fill missing values, and export clean sheets.

[![Deploy to Hostinger](https://hostinger.com/deploy-button.svg)](https://hostinger.com?REFERRAL_CODE_HERE)

## Features
- Upload CSV or Excel (`.xlsx`, `.xls`) files
- Automatic text whitespace stripping
- Snake_case column formatting
- Custom duplicate & NaN removal
- Instant export to Excel or CSV

## Run Locally
```bash
git clone [https://github.com/DiscoverTalent/excel-cleaner-app.git](https://github.com/DiscoverTalent/excel-cleaner-app.git)
cd excel-cleaner-app
pip install -r requirements.txt
streamlit run app.py
