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


