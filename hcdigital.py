from selenium import webdriver
import pandas as pd
import time
import xlsxwriter
from selenium.webdriver.chrome.options import Options
profile = pd.DataFrame(columns = ['Name', 'Address', 'City', 'State', 'Country', 'Unique Amenity', 'PrimaryImageURL', 'Webpage'])
chrome_options = Options()  
chrome_options.add_argument("--headless")
chrome_options.binary_location = r'C:\Users\saqib\AppData\Local\Google\Chrome SxS\Application\chrome.exe'
browser = webdriver.Chrome(options=chrome_options)
url = 'https://www.signaturetravelnetwork.com/microsites/index.cfm?pageaction=offer-listing&utp=consumer&type=consumer&agency_id=1133&agent_id=0&client_id=0&campaign_id=0&cid=0&site_id=12&srchByArea=0&srchByCountry=0&srchByState=0&srchByCity=0&srchByAirport=0'
urls = [1,2,3,4,5,6,7,8,9]
urls[0] = 'https://www.hcdigitaldirectory.com/regions?region=US'
urls[1] = 'https://www.hcdigitaldirectory.com/regions?region=CA'
urls[2] = 'https://www.hcdigitaldirectory.com/regions?region=MX'
urls[3] = 'https://www.hcdigitaldirectory.com/regions?region=BC'
urls[4] = 'https://www.hcdigitaldirectory.com/regions?region=CM'
urls[5] = 'https://www.hcdigitaldirectory.com/regions?region=SA'
urls[6] = 'https://www.hcdigitaldirectory.com/regions?region=EU'
urls[7] = 'https://www.hcdigitaldirectory.com/regions?region=ME'
urls[8] = 'https://www.hcdigitaldirectory.com/regions?region=AP'
count = 0
for url in urls[8:]:
    print(url)
    browser.get(url)
    brands = browser.find_elements_by_xpath("//h4[@class='panel-title statelinkPanel']")
    hrefs = []
    for b in brands:
        hrefs.append(b.find_element_by_tag_name('a').get_attribute('href'))
    for link in hrefs:
        browser.get(link)
        hotels = browser.find_elements_by_xpath("//a[@class='fresult-prop-name-link']")
        hotel = []
        for h in hotels:
            hotel.append(h.get_attribute('href'))
        for hot in hotel:
            count += 1
            browser.get(hot)
            name = browser.find_element_by_xpath("//h1[@class='book hotelName']").text
            place = browser.find_element_by_xpath("//div[@class='shade']").find_element_by_tag_name('h2').text.split(', ')
            if(len(place) == 3):
                city = place[0]
                state = place[1]
                country = place[2]
            else:
                city = place[0]
                country = place[1]
                state = ''
            amenities = browser.find_element_by_xpath("//ul[@class='book']").text.replace('\n', ' ')
            address = browser.find_element_by_xpath("//span[@class='span1 addresspan ']").text.split(',')[0]
            image = 'https://www.hcdigitaldirectory.com' + browser.find_element_by_xpath("//div[@class='col-sm-12 col-md-12 propTop']").get_attribute('style').split('("')[1].split('")')[0]
            print('Record No: {} scraped whose name is: {}'.format(count, name))
            ser = pd.Series([name, address, city, state, country, amenities, image, hot], index = ['Name', 'Address', 'City', 'State', 'Country', 'Unique Amenity', 'PrimaryImageURL', 'Webpage'])
            profile = profile.append(ser, ignore_index = True)
filename = 'out.xlsx'
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
profile.to_excel(writer, index=False)
writer.save()  

    
    

    
    
