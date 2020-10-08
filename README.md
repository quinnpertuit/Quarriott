# Quarriott

Quarriott is a Python command line tool for fetching + comparing hotel prices for a variety of corporate codes. 

## Requirements
Python 3
```bash
pip install -r requirements.txt
```

## Usage
From the command line
```python
python3 run.py --help
```

Example
```bash
python3 marriott.py \
  --system_os "Linux" \ 
  --checkin "Dec 10" \
  --checkout "Dec 11" \
  --location "Denver, CO" \
  --test 1
```

![Demo](https://github.com/quinnpertuit1/Quarriott/raw/main/docs/demo.jpeg)

## Notes
The system_os input argument is used in performing action keys to clear the search input elements depending on your operating system. 

## Disclaimer
This repository / project is purely intended for educational and academic purposes. This project and corresponding modules should not be used for any purpose other than learning. Scraping the websites or using the demo material in this repo may be a violation of site policies. Check the terms and conditions of use for any websites you intend to scrape. Use at your own risk. 
