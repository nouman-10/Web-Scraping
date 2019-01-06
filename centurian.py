from selenium import webdriver
import pandas as pd
import time
import xlsxwriter
from selenium.webdriver.chrome.options import Options
chrome_options = Options()  
chrome_options.add_argument("--headless")  
browser = webdriver.Chrome(options=chrome_options)
profile = pd.DataFrame(columns = ['Name', 'Address', 'City', 'Country', 'NearestAirport', 'CenturianAmenities', 'Webpage'])
url = 'https://centurionfhrdirectory.com/CenturionProperties'
browser.get(url)
time.sleep(20)
links = browser.find_elements_by_xpath("//div[@class='partnerBox clickLink']")
hrefs = []
count = 0
for i in links:
    hrefs.append(i.find_element_by_tag_name('a').get_attribute('href'))
for link in hrefs:
    count += 1
    browser.get(link)
    time.sleep(1)
    name = browser.find_element_by_xpath("//div[@class='shade']").find_element_by_tag_name('h1').text
    cityCountry = browser.find_element_by_xpath("//h2[@class='headcity']").text
    index = cityCountry.rfind(',')
    city = cityCountry[:index]
    country = cityCountry[index+2:]
    amenities = browser.find_element_by_xpath("//ul[@class='cent-member-benefits']").text.replace('\n', ' ')
    address = browser.find_element_by_xpath("//span[@class='span1 addresspan ']").text.split(',')[0]
    airport = browser.find_element_by_xpath("//span[@class='airport']").text
    ser = pd.Series([name, address, city, country, airport, amenities, link], index = ['Name', 'Address', 'City', 'Country', 'NearestAirport', 'CenturianAmenities', 'Webpage'])
    profile = profile.append(ser, ignore_index = True)
    print('Records Scraped: {}'.format(count))
filename = 'output1.xlsx'
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
profile.to_excel(writer, index=False)
writer.save()  
