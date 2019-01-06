from selenium import webdriver
import pandas as pd
import time
import xlsxwriter
from selenium.webdriver.chrome.options import Options
profile = pd.DataFrame(columns = ['Name', 'Address', 'City', 'State', 'Country', 'NearbyAirport', 'ProgramAmenities', 'PrimaryImageURL', 'Webpage'])
chrome_options = Options()  
chrome_options.binary_location = r'C:\Users\saqib\AppData\Local\Google\Chrome SxS\Application\chrome.exe'

browser = webdriver.Chrome(options=chrome_options)
browser2 = webdriver.Chrome(options=chrome_options)
url = 'https://www.virtuoso.com/hotels#CurrentPage=1&FacetCategoryIndex=0&FacetLimit=6&LeftToShow=0&RowsPerPage=25&HotelBookingNumberChildren=0&HotelBookingNumberAdults=2&SearchType=Property&SearchView=1col&SortType=HotelNameAsc&StartRow=0'
browser2.get(url)
time.sleep(20)
count = 0

for i in range(1, 55):
    print('On Page No. : {}'.format(i))
    hrefs = []
    links = browser2.find_elements_by_xpath("//h2[@class='truncate-content-dotdot catalog-card__title']")
    
    for i in links:
        hrefs.append(i.find_element_by_tag_name('a').get_attribute('href'))
    len(hrefs)
    for link in hrefs:
        count += 1
        browser.get(link)
        name = browser.find_element_by_id('titleName').text
        amenities = browser.find_element_by_id('amenities-content').text.replace('\n', ' ')
        addresses = browser.find_elements_by_xpath("//div[@class='address']")
        address = addresses[0].text
        cityState = addresses[3].text.split(',')
        if(len(cityState) == 2):
            city = cityState[0]
            state = cityState[1]
            state = state.split(' ')[0]
            country = addresses[4].text
        elif(len(cityState) > 2):
            city = cityState[0]
            state = cityState[1]
            country = cityState[2]
        airport = browser.find_elements_by_class_name('field-value')
        if(len(airport) > 1):
            airport = airport[1].text
        else:
            airport = airport[0].text
        imgUrl = browser.find_elements_by_xpath("//div[@class='galleria-image']")[1].find_element_by_tag_name('img').get_attribute('src')
        rooms = browser.find_element_by_xpath("//span[@class='info-label']").text.split(': ')[1].split(' ')[0]
        ser = pd.Series([name, address, city, state, country, airport, amenities, imgUrl, link], index = ['Name', 'Address', 'City', 'State', 'Country', 'NearbyAirport', 'ProgramAmenities', 'PrimaryImageURL', 'Webpage'])
        profile = profile.append(ser, ignore_index = True)
        print('Records Scraped: {} whose name is {}'.format(count, name))
    if(i != 54):
        nextt = browser2.find_element_by_xpath("//a[@class='next']")
        nextt.click()
        time.sleep(3.5)
    
filename = 'output5.xlsx'
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
profile.to_excel(writer, index=False)
writer.save()     
