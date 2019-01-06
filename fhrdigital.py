from selenium import webdriver
import pandas as pd
import time
import xlsxwriter
from selenium.webdriver.chrome.options import Options
profile = pd.DataFrame(columns = ['Name', 'Address', 'City', 'State', 'Country', 'NearestAirport',  'Unique Amenity', 'PrimaryImageURL', 'Webpage'])
chrome_options = Options()  
chrome_options.add_argument("--headless")
chrome_options.binary_location = r'C:\Users\saqib\AppData\Local\Google\Chrome SxS\Application\chrome.exe'
browser = webdriver.Chrome(options=chrome_options)
browser.get('https://fhrdigitaldirectory.com/property-results/r/1,2,3,4,5,6,7,8,9')
count = 0
links = browser.find_elements_by_xpath("//a[@class='property-card']")
hrefs = []
for l in links:
    hrefs.append(l.get_attribute('href'))
for link in hrefs:
    browser.get(link)
    name = browser.find_element_by_xpath("//h1[@class='pt-supplierName']").text
    place = browser.find_element_by_xpath("//div[@class='pt-location']").text
    city, stat = place.split(', ')
    stat = stat.split(' ')
    if(len(stat) > 1):
        country = stat[1]
        state = stat[0]
    else:
        country = stat[0]
        state = city
    airport, address = browser.find_element_by_xpath("//p[@class='pl-airport']").text, browser.find_element_by_xpath("//p[@class='pl-location']").text
    image = browser.find_element_by_xpath("//div[@class='top-hero']").get_attribute('style').split('("')[1].split('")')[0]
    amenity = browser.find_element_by_class_name('pi-special-benefit').find_element_by_tag_name('p').text
    count += 1
    print('Record No: {} scraped. Name: {}'.format(count, name))
    ser = pd.Series([name, address, city, state, country, airport, amenity, image, link], index = ['Name', 'Address', 'City', 'State', 'Country', 'NearestAirport',  'Unique Amenity', 'PrimaryImageURL', 'Webpage'])
    profile = profile.append(ser, ignore_index = True)
filename = 'fhrdigital.xlsx'
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
profile.to_excel(writer, index=False)
writer.save()  

    
    

    
    
