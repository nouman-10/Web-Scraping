from selenium import webdriver
import pandas as pd
import time
import xlsxwriter
from selenium.webdriver.chrome.options import Options
profile = pd.DataFrame(columns = ['HotelName', 'Address', 'City', 'Country', 'NearestAirport', 'PropertySize', 'ProgramAmenities', 'Webpage', 'Webpage2', 'PrimaryImageURL'])
chrome_options = Options()  
chrome_options.add_argument("--headless")
chrome_options.binary_location = r'C:\Users\saqib\AppData\Local\Google\Chrome SxS\Application\chrome.exe'
browser = webdriver.Chrome(options=chrome_options)
url = 'https://www.signaturetravelnetwork.com/microsites/index.cfm?pageaction=offer-listing&utp=consumer&type=consumer&agency_id=1133&agent_id=0&client_id=0&campaign_id=0&cid=0&site_id=12&srchByArea=0&srchByCountry=0&srchByState=0&srchByCity=0&srchByAirport=0'

counter = 1
count = 0
for j in range(1,38):
    browser.get(url)
    time.sleep(10)
    page = browser.find_elements_by_xpath("//a[@class='pagerLink']")
    page[counter].click()
    if(counter > 5 and j < 35):
        counter = 5
    else:
        counter += 1;
    links = browser.find_elements_by_xpath("//div[@class='row searchResult']")
    hrefs = []
    for i in links:
        hrefs.append(i.find_element_by_tag_name('a').get_attribute('href'))
    for link in hrefs:
        count += 1
        browser.get(link)
        header = browser.find_element_by_xpath("//section[@class='title-row']").find_element_by_tag_name('h1')
        name, cityCountry = header.text.split('\n')
        index = cityCountry.rfind(',')
        city = cityCountry[:index]
        country = cityCountry[index+2:]
        address = browser.find_element_by_xpath("//div[@class='hotel-descr']").find_element_by_tag_name('p').text
        address = address.split('\n')[1]
        amenities = browser.find_element_by_xpath("//div[@class='amenities_div']").text
        amenities = amenities.replace('\n', ' ')
        image = browser.find_element_by_xpath("//img[@class='main-image']")
        imgUrl = image.get_attribute('src')
        accomm = browser.find_elements_by_xpath("//li[@class='hovernav']")
        accomm[3].click()
        rooms = browser.find_element_by_xpath("//div[@class='col-md-12 twoColumn']").find_element_by_tag_name('b')
        size = rooms.text.split(': ')[1]
        accomm = browser.find_elements_by_xpath("//li[@class='hovernav']")
        accomm[6].click()
        a = browser.find_element_by_xpath("//div[@class='col-md-4']")
        nearby = a.text.split('Nearby Airports')[1]
        print('Record No: {} scraped'.format(count))
        link1, link2 = link[0:250], link[250:]
        ser = pd.Series([name, address, city, country, nearby, size, amenities, link1, link2, imgUrl], index = ['HotelName', 'Address', 'City', 'Country', 'NearestAirport', 'PropertySize', 'ProgramAmenities', 'Webpage', 'Webpage2', 'PrimaryImageURL'])
        profile = profile.append(ser, ignore_index = True)
filename = 'output.xlsx'
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
profile.to_excel(writer, index=False)
writer.save()  

    
    

    
    
