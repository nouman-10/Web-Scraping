from selenium import webdriver
import pandas as pd
import time
import xlsxwriter
from selenium.webdriver.chrome.options import Options
profile = pd.DataFrame(columns = ['Name', 'Address', 'City', 'Country', 'Unique Amenities',  'PrimaryImageURL', 'Webpage'])
chrome_options = Options()  
chrome_options.add_argument("--headless")  
browser = webdriver.Chrome(options=chrome_options)
url = 'https://www.visasignaturehotels.com/search?referrer=&preferredCurrencyId=&numAdults=2&numChildren=0&submitButton=&rows=20&page={}&sortBy=relevancy&getSpecialOffers=1&analyticsId=6b9855dcda0bc24f092b478aa7e094a6'
count = 0
for i in range(45,47):
    browser.get(url.format(i))
    time.sleep(2)
    hrefs = []
    links = browser.find_elements_by_xpath("//a[@class='results-list-item-link']")
    for l in links:
        hrefs.append(l.get_attribute('href'))
    for link in hrefs:
        count += 1
        browser.get(link)
        name = browser.find_element_by_xpath("//div[@class='header-title subheader']").find_element_by_tag_name('h1').text.split(',')[0]
        place = browser.find_elements_by_xpath("//li[@property='itemListElement']")
        if(len(place) > 3):
            country = place[1].text
            city = place[3].text
            if(country == 'United Kingdom'):
                country = place[2].text
        else:
            country = place[1].text
            city = place[2].text
        address = browser.find_element_by_xpath("//ul[@class='subheading']").find_element_by_tag_name('li').text
        benefits = browser.find_element_by_xpath("//ul[@class='benefits ']").text.replace('\n', ' ')
        image = browser.find_element_by_xpath("//div[@class='carousel-image-wrapper']")
        imgUrl = image.find_element_by_tag_name('img').get_attribute('src')
        ser = pd.Series([name, address, city, country, benefits, imgUrl, link], index = ['Name', 'Address', 'City', 'Country', 'Unique Amenities',  'PrimaryImageURL', 'Webpage'])
        profile = profile.append(ser, ignore_index = True)
        print('Records Scraped: {}'.format(count))
filename = 'output4.xlsx'
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
profile.to_excel(writer, index=False)
writer.save()     
