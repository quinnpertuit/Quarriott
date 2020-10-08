# Quarriott

Quarriott is a Python command line tool for fetching + comparing hotel prices for a variety of corporate codes. 

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

## Example
```bash

python3 marriott.py -s Linux -i "Dec 10" -o "Dec 11" -l "Denver, CO" -t 1

python3 marriott.py \
  --system_os "Linux" \ 
  --checkin "Dec 10" \
  --checkout "Dec 11" \
  --location "Denver, CO" \
  --test 1
```
Output is saved as a csv in the output folder.

## Command Line Tool
![Demo](https://github.com/quinnpertuit1/Quarriott/raw/main/docs/demo.png)

## Demo Output Visual
![Vis](https://github.com/quinnpertuit1/Quarriott/raw/main/docs/vis.gif)

## Notes
The system_os input argument is used in performing action keys to clear the search input elements depending on your operating system. 

## Disclaimer
This repository / project is purely intended for educational and academic purposes. This project and corresponding modules should not be used for any purpose other than learning. Scraping the websites or using the demo material in this repo may be a violation of site policies. Check the terms and conditions of use for any websites you intend to scrape. Use at your own risk. 
