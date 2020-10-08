from selenium import webdriver
import chromedriver_autoinstaller 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains 

chromedriver_autoinstaller.install()

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
