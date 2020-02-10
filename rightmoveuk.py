# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 23:34:22 2020

@author: nouma
"""

from selenium import webdriver
import pandas as pd
from selenium.webdriver.firefox.options import Options
import json

def start_browser(headless):
    print('Starting the Browser')
    options = Options()
    if(headless):
        options.add_argument('--headless')
    browser =  webdriver.Firefox(options=options, executable_path=r'C:\Users\nouma\Downloads\geckodriver.exe')
    return browser
    

def read_zipcodes():
    zipcodes = {}
    url="https://en.wikipedia.org/wiki/List_of_postcode_districts_in_the_United_Kingdom"
    browser.get(url)
    time.sleep(5)
    table = browser.find_element_by_xpath("//table[@class = 'wikitable sortable jquery-tablesorter']")
    My_row = table.find_elements_by_tag_name('tr')
    for row in My_row[1:]:
        zips = row.find_elements_by_tag_name('td')[1].text.replace('\n','').replace('non-geo','').replace('shared','')
        for i in range(1,20):
            zips = zips.replace('non-geo[{}]'.format(i),'').replace('shared[{}]'.format(i),'').replace('[{}]'.format(i),'')
        zips = zips.split(',')
        town = row.find_elements_by_tag_name('td')[2].text
        for zipcode in zips:
            zipc = zipcode.strip()
            zipcodes[zipc] = [town]
    return list(zipcodes.keys())
        
def read_outcodes(zipcodes):
    outcodes = {}
    for zipcode in zipcodes:
        browser.get(outcodes_url.format(zipcode))
        try:
            browser.find_element_by_id('submit').click()
        except:
            continue
        current_url = browser.current_url
        start_index = current_url.find('OUTCODE%5E')
        end_index = current_url[start_index+10:].find('&')
        outcode = current_url[start_index+10:end_index+start_index+10]
        outcodes[zipcode] = outcode
        if(len(outcodes) % 100 == 0):
            print('{} done'.format(len(outcodes)))
    return outcodes


def read_outcodes_from_files(file_name):
    json_file = open(file_name, 'r')
    json_data = json.loads(json_file.read())
    return json_data

def scrape_number_of_records(url, outcode, bedrooms, let_agreed):
    browser.get(url.format(outcode, bedrooms, bedrooms, let_agreed))
    records = browser.find_element_by_xpath("//span[@class='searchHeader-resultCount']").text
    return records


def create_df():
    return pd.DataFrame(columns=['Post Code', 'General', 'Studio', '1 Bedroom', '2 Bedrooms', '3 Bedrooms', '4 Bedrooms', '5 Bedrooms', '6 Bedrooms', '7 Bedrooms'])

def create_series(total_demand):
    houses_ser =  pd.Series([zipcode, total_demand[0][0], total_demand[1][0], total_demand[2][0], total_demand[3][0], total_demand[4][0], total_demand[5][0], total_demand[6][0], total_demand[7][0], total_demand[8][0]], index = houses_df.columns)    
    flats_ser = pd.Series([zipcode, total_demand[0][1], total_demand[1][1], total_demand[2][1], total_demand[3][1], total_demand[4][1], total_demand[5][1], total_demand[6][1], total_demand[7][1], total_demand[8][1]], index = houses_df.columns)    
    return houses_ser, flats_ser

def write_to_excel():
    with pd.ExcelWriter('output.xlsx') as writer:  
        houses_df.to_excel(writer, sheet_name='houses')
        flats_df.to_excel(writer, sheet_name='flats')
        
def calculate_demand(url, outcode, bedrooms):
    try:
        with_let = int(scrape_number_of_records(url, outcode, bedrooms, 'true'))
        without_let = int(scrape_number_of_records(url, outcode, bedrooms, 'false'))
        demand = round(without_let / with_let, 2)
    except:
        demand = 0
    return demand

        
browser = start_browser(True)
outcodes_url = 'https://www.rightmove.co.uk/property-to-rent/search.html?searchLocation={}&locationIdentifier=&useLocationIdentifier=false&rent=To+rent'
url = 'https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=OUTCODE%5E1862&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare='

zipcodes = read_zipcodes()
outcodes = read_outcodes(zipcodes)

#json_data = json.dumps(outcodes)
#f = open("outcodes.json","w")
#f.write(json_data)
#f.close()

#outcodes = read_outcodes_from_files('outcodes.json')
houses_url = 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=OUTCODE%5E{}&maxBedrooms={}&minBedrooms={}&propertyTypes=bungalow%2Cdetached%2Csemi-detached%2Cterraced&includeLetAgreed={}&mustHave=&dontShow=&furnishTypes=&keywords='
flats_url = 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=OUTCODE%5E{}&maxBedrooms={}&minBedrooms={}&propertyTypes=flat&primaryDisplayPropertyType=flats&includeLetAgreed={}&mustHave=&dontShow=&furnishTypes=&keywords='
    
urls = [houses_url, flats_url]    

houses_df = create_df()
flats_df = create_df()

for zipcode, outcode in outcodes.items():
    total_demand = [[calculate_demand(url, outcode, '' if i == 0 else i - 1) for url in urls] for i in range(9)]
    houses_series, flats_series = create_series(total_demand)
    houses_df = houses_df.append(houses_series, ignore_index=True)
    flats_df = flats_df.append(flats_series, ignore_index=True)
    print('General Demand for houses in zipcode {} is {}'.format(zipcode, total_demand[0][0]))
    try:
        write_to_excel()
    except:
        pass
        
        
    
        
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
