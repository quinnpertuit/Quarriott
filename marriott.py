import sys
import os
import time
import argparse
import selenium
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from selenium import webdriver
import chromedriver_autoinstaller 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains 

# https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_win32.zip

parser = argparse.ArgumentParser(prog="""\n
 .d88888b.                               d8b        888   888   
d88P" "Y88b                              Y8P        888   888   
888     888                                         888   888   
888     888888  888 8888b. 888d888888d888888 .d88b. 888888888888
888     888888  888    "88b888P"  888P"  888d88""88b888   888   
888 Y8b 888888  888.d888888888    888    888888  888888   888   
Y88b.Y8b88PY88b 888888  888888    888    888Y88..88PY88b. Y88b. 
 "Y888888"  "Y88888"Y888888888    888    888 "Y88P"  "Y888 "Y888
       Y8b                                                      \n\nQuarriott - the Marriott Fetcher""", description='Fetch Marriott hotel prices for a location and dates.\nRuns a batch of corporate codes to collect and compare rates.', usage='%(prog)s [options]')

parser.add_argument('-s','--system_os', help='Windows, OSX, or Linux', required=True)
parser.add_argument('-i','--checkin', help='Check-in date (e.g. "Oct 17")', required=True)
parser.add_argument('-o','--checkout', help='Check-out date (e.g. "Oct 18")', required=True)
parser.add_argument('-l','--location', help='Location (examples: "Nashville", "Nashville, TN", "2500 West End Ave, Nashville, TN")', required=True)
parser.add_argument('-t','--test', help='Enter 1 to run test only, 0 to run full. Test runs one search.', required=True)
args = vars(parser.parse_args())


## Function to setup and prepare webdriver
def prepare_driver():
    url = "https://www.marriott.com/search/default.mi"
    
    try:
        options = webdriver.ChromeOptions() 
        options.add_argument('--headless')
        options.add_argument('--profile-directory=Default') 
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'destinationAddress.destination')))
        print("DRIVER:  "+"Chrome webdriver initialization and launch successful.")

    except:
        print("DRIVER:  "+"Chrome webdriver initialization failed. See prepare_driver function.")
        exit()

    return(driver)

## Function to perform search with webdriver
def perform_search(driver, system_in, location, checkin, checkout, use_code, rate_code, rate_company):
        print("FETCHING: " + location + " | Run Date: " + datetime.now().strftime("%Y-%m-%d") + " | In: " , checkin , " | Out: " + checkout + " | Company: " + rate_company + " | Code: "+rate_code)
        
        ## Input search location into web element
        try:
            search_location = driver.find_element_by_name('destinationAddress.destination')
            search_location.click()
            search_location.clear()
            search_location.send_keys(location)
            time.sleep(1)
        except: 
            print("SKIPPING: "+rate_company+" ("+rate_code+")"+" location input failed for '"+location+"'.\nRecovering...")

        ## Input check-in date into web element
        try:
            search_checkin = driver.find_element_by_class_name('ccheckin')

            if (system_in=='Windows'):
                search_checkin.click()
                search_checkin.send_keys(Keys.CONTROL + "a")
                search_checkin.send_keys(Keys.BACKSPACE)
                search_checkin.send_keys(checkin)
                search_checkin.send_keys(Keys.ESCAPE)
            else:
                search_checkin = driver.find_element_by_class_name('ccheckin')
                search_checkin.send_keys(Keys.ESCAPE)
                search_checkin.click()
                action = ActionChains(driver) 
                action.double_click(on_element = search_checkin) 
                action.perform() 
                search_checkin.send_keys(Keys.BACKSPACE);
                search_checkin.send_keys(checkin)
        except: 
            print("SKIPPING: "+rate_company+" ("+rate_code+")"+" check-in date input failed for '"+checkin+"'.\nRecovering...")

        ## Input check-out date into web element
        try:
            search_checkout = driver.find_element_by_class_name('ccheckout')

            if (system_in=='Windows'):
                search_checkout.click()
                search_checkout.send_keys(Keys.CONTROL + "a")
                search_checkout.send_keys(Keys.BACKSPACE)
                search_checkout.send_keys(checkout)
                search_checkout.send_keys(Keys.ESCAPE)
            else:
                search_checkout = driver.find_element_by_class_name('ccheckout')
                search_checkout.send_keys(Keys.ESCAPE)
                search_checkout.click()
                action = ActionChains(driver) 
                action.double_click(on_element = search_checkout) 
                action.perform() 
                search_checkout.send_keys(Keys.BACKSPACE);
                search_checkout.send_keys(checkout)
                search_checkout.send_keys(Keys.ENTER)
        except: 
            print("SKIPPING: "+rate_company+" ("+rate_code+")"+" check-out date input failed for '"+checkout+"'.\nRecovering...")

        ## Input rate code into web element
        try:
            if use_code:
                search_ratecode = driver.find_element_by_class_name('js-special-rates-header')
                search_ratecode.click()
                time.sleep(1)
                if use_code == '1':
                    search_ratecodecorporate = driver.find_element_by_xpath("//label[contains(text(),'Corporate')]")
                    search_ratecodecorporate.click()
                    if rate_code:
                        driver.find_element_by_name("corporateCode").send_keys(str(rate_code))
        except: 
            print("SKIPPING: "+rate_company+" ("+rate_code+")"+" special rate code input failed.\nRecovering...")

        ## Submit search
        try:
            driver.find_element_by_css_selector("div.l-hsearch-find button").click()
            time.sleep(1)
        except: 
            print("SKIPPING: "+rate_company+" ("+rate_code+")"+" final search execution failed.\nRecovering...")


## Function to parse and prepare webdriver
def parse_results(driver, rate_code, rate_company, location, checkin, checkout):

    print("PARSING:  " + location + " | Run Date: " + datetime.now().strftime("%Y-%m-%d") + " | In: " , checkin , " | Out: " + checkout + " | Company: " + rate_company + " | Code: "+rate_code)

    hotel_names = list()
    hotel_links = list()
    hotel_address = list()
    hotel_price = list()
    dist = list()
    
    try:
        hotel_names_driver = driver.find_elements_by_class_name("l-property-name")
        
        for hotel in hotel_names_driver:
            hotel_names.append(hotel.text)
        hotel_links_driver = driver.find_elements_by_class_name("js-hotel-quickview-link")
        for hotel in hotel_links_driver:
            hotel_links.append(hotel.get_attribute('href'))
        hotel_address_driver = driver.find_elements_by_class_name("m-hotel-address")
        for hotel in hotel_address_driver:
            hotel_address.append(hotel.text)
        hotel_price_driver = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "l-margin-three-quarters", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "l-sold-out", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "m-display-block", " " ))]')
        for hotel in hotel_price_driver:
            hotel_price.append(hotel.text)
        
        hotel_price = np.array(hotel_price)
        hotel_price = hotel_price[hotel_price!=''].tolist()
        
        out = pd.DataFrame({'hotel':hotel_names,'address':hotel_address,'price':hotel_price})
        
        out['code']=rate_code
        out['company']=rate_company
        out['run_date']=datetime.now().strftime("%Y-%m-%d")
        out['location']=location
        out['checkin']=checkin
        out['checkout']=checkout
        
        out = out[['company','code','hotel','price','location','run_date','checkin','checkout','address']]
        print("PULLED:   " + rate_company + " (" + rate_code + ")" + " results appended to output data frame.")
        driver.close()


    except:
        driver.close()
        print("SKIPPING: "+rate_company+" ("+rate_code+")"+"\nRecovering...")
        out = pd.DataFrame()

    return(out)

## Load in corporate rate codes from csv or using in-line data frame below or codes_in = pd.read_csv('marriott-rate-codes.csv', index_col=False)
codes_in = pd.DataFrame({
            'company': {0: '3M', 1: 'AAA', 2: 'AARP', 3: 'Accenture', 4: 'Advance Purchase Rate',5: 'Aetna',
                        6: 'Alaska Airlines',7: 'Allstate', 8: 'American Express', 9: 'Apple', 10: 'AT&T',
                        11: 'Bank of America', 12: 'Best Available Rate', 13: 'Boeing', 14: 'Chick-Fil-A', 15: 'Chrysler',
                        16: 'Citi', 17: 'Coca-Cola', 18: 'COX', 19: 'Dell', 20: 'Deloitte', 
                        21: 'Delta', 22: 'Disney', 23: 'Exxon', 24: 'FedEx', 25: 'Ford', 
                        26: 'GAP', 27: 'General Corporate Rate', 28: 'General Electric', 29: 'GM', 30: 'Google',
                        31: 'Government Rate', 32: 'IBM', 33: 'Intel', 34: 'JCPenney', 35: 'JPMorgan',
                        36: 'Kroger', 37: 'Leisure Rate', 38: 'Local Promotion Rate', 39: 'Lockheed Martin', 
                        40: 'Look No Further Rate', 41: 'Lowes', 42: 'Microsoft', 43: 'Morgan Stanley', 44: 'Nike', 45: 'Nissan', 
                        46: 'Northrop Grumman', 47: 'Oracle', 48: 'Pepsi', 49: 'Pfizer', 50: 'Proctor & Gamble', 
                        51: 'Prudential', 52: 'Qualcomm', 53: 'Raytheon', 54: 'SAP', 55: 'Shell', 
                        56: 'Sony', 57: 'Southwest Airlines', 58: 'Sprint', 59: 'Sun Microsystems', 60: 'Texas Instruments',
                        61: 'ThyssenKrupp', 62: 'Toshiba', 63: 'Toyota', 64: 'United Airlines', 65: 'UPS',
                        66: 'Wedding Rate', 67: 'Wells Fargo'},
            'code':    {0: 'MMM', 1: 'AAA', 2: 'ARP', 3: 'ACC', 4: 'ADP', 5: 'AET', 6: 'A70', 7: 'ALL', 8: 'AMX', 9: 'APL', 10: 'ATT',
                        11: 'BOA', 12: 'BAR', 13: 'BOE', 14: 'CFA', 15: 'DCX', 16: 'CIT', 17: 'COK', 18: 'COX', 19: 'DEL', 20: 'DTC', 
                        21: 'DLA', 22: 'DIS', 23: 'XOM', 24: 'FED', 25: 'FRD', 26: 'GAP', 27: 'CRP', 28: 'GEE', 29: 'GMC', 30: 'GGL',
                        31: 'GOV', 32: 'IBM', 33: 'INL', 34: 'JCP', 35: 'JPM', 36: 'KRO', 37: 'LRR', 38: 'LPR', 39: 'XML', 40: 'LNF', 
                        41: 'LOW', 42: 'MCO', 43: 'MOS', 44: 'NKE', 45: 'NIS', 46: 'NOR', 47: 'ORA', 48: 'PEP', 49: 'PFE', 50: 'PAG', 
                        51: 'PRU', 52: 'QUA', 53: 'RAY', 54: 'SAP', 55: 'SHL', 56: 'SON', 57: 'SW8', 58: 'SPR', 59: 'SUN', 60: 'TXI',
                        61: 'TSN', 62: 'TOS', 63: 'TOY', 64: 'UAL', 65: 'UPS', 66: 'W14', 67: 'WEL'}})

## Parse user command-line inputs
system_input = args['system_os']   # Linux
check_in     = args['checkin']  # 'Oct 17'
check_out    = args['checkout'] # 'Oct 18'
location_in  = args['location'] # 'Ooltewah, TN'
run_test     = args['test']     # 0

## If user-input args['test'] = 1, run one company search as a test.
if run_test=="1":

    start_time = time.time()
    allOut = pd.DataFrame()
    company = 'AAA Travel'
    code = 'AAA'

    try:
        driver = prepare_driver()
        perform_search(driver = driver, system_in = system_input, location=location_in, checkin=check_in, checkout=check_out, use_code='1', rate_code=code, rate_company=company)
        output = parse_results(driver, location=location_in, checkin=check_in, checkout=check_out, rate_code=code, rate_company=company)
        allOut = allOut.append(output, ignore_index=True)
        driver.close()

    except:
        print("SKIPPING: "+company+" ("+code+")"+"\nRecovering...")
            
    fname = './output/tests/'+datetime.now().strftime("%m-%d-%Y-%H%M%S")+' '+location_in+'.csv'

    end_time = time.time()

    print("WRITING:  Results saving to file '"+fname+"'")
    allOut.to_csv(fname, index = False, header=True)

    run_duration = end_time-start_time

    if(run_duration>=60):
        run_duration = str(round(run_duration/60)) + " minute(s)."
    else:
        run_duration = str(round(run_duration)) + " seconds."

    print("COMPLETE: Total run time: "+run_duration)


## Run full production process
else:

    start_time = time.time()
    allOut = pd.DataFrame()

    for index, row in codes_in.iterrows():
            company = str(row['company'])
            code = str(row['code'])
            try:
                driver = prepare_driver()
                perform_search(driver = driver, system_in = system_input, location=location_in, checkin=check_in, checkout=check_out, use_code='1', rate_code=code, rate_company=company)
                output = parse_results(driver, location=location_in, checkin=check_in, checkout=check_out, rate_code=code, rate_company=company)
                allOut = allOut.append(output, ignore_index=True)
            except:
                driver.close()
                print("SKIPPING: "+company+" ("+code+")"+"\nRecovering...")
                
    fname = './output/'+datetime.now().strftime("%m-%d-%Y-%H%M%S")+' '+location_in+'.csv'

    end_time = time.time()

    print("WRITING:  Results saving to file '"+fname+"'")

    allOut.to_csv(fname, index = False, header=True)

    run_duration = end_time-start_time

    if(run_duration>=60):
        run_duration = str(round(run_duration/60)) + " minute(s)."
    else:
        run_duration = str(round(run_duration)) + " seconds."

    print("COMPLETE: Total run time: "+run_duration)

time.sleep(0.5)
driver.quit()

