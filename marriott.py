import sys
import os
import time
import argparse
import selenium
from datetime import datetime, timedelta
from sys import platform
import numpy as np
import pandas as pd
from main.driver import *
from main.search import *
from main.codes import *
from main.parse import *

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

parser.add_argument('-i','--checkin', help='Check-in date (e.g. "Oct 17")', required=True)
parser.add_argument('-o','--checkout', help='Check-out date (e.g. "Oct 18")', required=True)
parser.add_argument('-l','--location', help='Location (examples: "Nashville", "Nashville, TN", "2500 West End Ave, Nashville, TN")', required=True)
parser.add_argument('-t','--test', help='Enter 1 to run test only, 0 to run full. Test runs one search.', required=True)
args = vars(parser.parse_args())

if platform == "linux" or platform == "linux2":
   system_input = 'Linux'
elif platform == "darwin":
   system_input = 'OSX'
elif platform == "win32":
   system_input = 'Windows'
  
## Parse user command-line inputs
check_in     = args['checkin']  # 'Oct 17'
check_out    = args['checkout'] # 'Oct 18'
location_in  = args['location'] # 'Denver, CO'
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

try: 
    driver.quit()
except:
    print("Driver closed.")

