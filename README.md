# Quarriott - Hotel Intel

Quarriott is a Python command line tool for fetching and comparing hotel rates for a variety of corporate codes. 

# Unrelated but Awesome

Unrelated, but equally awesome: [Unhidden Rates on Hotwire](https://q-ttt2.shinyapps.io/hotwire-unhidden/)

I don't maintain any of this. 

## Requirements
Python 3

## Installation 
```bash
git clone https://github.com/quinnpertuit1/Quarriott
cd Quarriott
pip3 install -r requirements.txt
```

Uses a headless chrome driver; if you don't have Chrome installed, run:
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt -y install ./google-chrome-stable_current_amd64.deb
```

## Usage
From the command line
```python
python3 marriott.py --help
```

## Examples
Run one test.
```bash

python3 marriott.py -i "Dec 10" -o "Dec 11" -l "Denver, CO" -t 1

```
Run full; fetches rates for all hotels around input location using 70 different corporate rate codes.
```bash
python3 marriott.py -i "Dec 10" -o "Dec 11" -l "Denver, CO" -t 0

python3 marriott.py \
  --checkin "Dec 10" \
  --checkout "Dec 11" \
  --location "Denver, CO" \
  --test 0
```

## Output
Output is saved as a csv in the output folder. Output from tests are saved in output/tests. 

**Click [here to view sample output csv](https://github.com/quinnpertuit1/Quarriott/blob/main/output/sample-output.csv).**


## Command Line Tool
![Demo](https://github.com/quinnpertuit1/Quarriott/raw/main/docs/demo.png)

## Demo Output Visual
![Vis](https://github.com/quinnpertuit1/Quarriott/raw/main/docs/vis.gif)

## Notes
This tool uses chromedriver_autoinstaller to automatically set up and configure your chrome web driver.

## Disclaimer
This repository / project is purely intended for educational and academic purposes. This project and corresponding modules should not be used for any purpose other than learning. Scraping the websites or using the demo material in this repo may be a violation of site policies. Check the terms and conditions of use for any websites you intend to scrape. Use at your own risk. 
