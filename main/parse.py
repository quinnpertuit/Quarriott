import selenium

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
