# Quarriott - Hotel Intel

Quarriott is a Python command line tool for fetching and comparing hotel rates for a variety of corporate codes. 

## Requirements
Python 3

## Installation 
```bash
git clone https://github.com/quinnpertuit1/Quarriott
cd Quarriott
pip3 install -r requirements.txt
```

## Usage
From the command line
```python
python3 marriott.py --help
```

## Examples
Run one test.
```bash

python3 marriott.py -s Linux -i "Dec 10" -o "Dec 11" -l "Denver, CO" -t 1

python3 marriott.py \
  --system_os "Linux" \ 
  --checkin "Dec 10" \
  --checkout "Dec 11" \
  --location "Denver, CO" \
  --test 1
```
Run full; fetches rates for all hotels around input location using 70 different corporate rate codes.
```bash
python3 marriott.py -s Linux -i "Dec 10" -o "Dec 11" -l "Denver, CO" -t 0
```

## Output
Output is saved as a csv in the output folder. Output from tests are saved in output/tests.

## Command Line Tool
![Demo](https://github.com/quinnpertuit1/Quarriott/raw/main/docs/demo.png)

## Demo Output Visual
![Vis](https://github.com/quinnpertuit1/Quarriott/raw/main/docs/vis.gif)

## Notes
The system_os input argument is used in performing action keys to clear the search input elements depending on your operating system. This repo uses chromedriver_autoinstaller to automatically set up and configure your chrome web driver.

## Disclaimer
This repository / project is purely intended for educational and academic purposes. This project and corresponding modules should not be used for any purpose other than learning. Scraping the websites or using the demo material in this repo may be a violation of site policies. Check the terms and conditions of use for any websites you intend to scrape. Use at your own risk. 
