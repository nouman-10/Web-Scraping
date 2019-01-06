#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 20:05:28 2018

@author: nouman
"""
import requests
import pandas as pd
import xlsxwriter 
from selenium import webdriver
import time
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from bs4 import BeautifulSoup

req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
profile = pd.DataFrame(columns=['Property Address', 'Owner Number'])

coutn = 0
urls = ['https://www.zillow.com/homes/fsbo/Collin-County-TX/951_rid/globalrelevanceex_sort/33.401638,-96.100159,32.982172,-97.038117_rect/9_zm/{}_p/0_mmm/', 'https://www.zillow.com/homes/fsbo/Denton-County-TX/988_rid/globalrelevanceex_sort/33.517354,-96.646729,32.898038,-97.584687_rect/9_zm/{}_p/0_mmm/','https://www.zillow.com/homes/fsbo/Dallas-County-TX/978_rid/globalrelevanceex_sort/33.077733,-96.308899,32.455314,-97.246857_rect/9_zm/{}_p/0_mmm/']
pages = [4,3,10]


def _is_element_displayed(driver, elem_text, elem_type):
    if elem_type == "class":
        try:
            out = driver.find_element_by_class_name(elem_text).is_displayed()
        except (NoSuchElementException, TimeoutException):
            out = False
    elif elem_type == "css":
        try:
            out = driver.find_element_by_css_selector(elem_text).is_displayed()
        except (NoSuchElementException, TimeoutException):
            out = False
    else:
        raise ValueError("arg 'elem_type' must be either 'class' or 'css'")
    return(out)

def _pause_for_captcha(driver):
    while True:
        if _is_element_displayed(driver, "captcha-container", "class"):
            continue
        elif _is_element_displayed(driver, "g-recaptcha", "class"):
            continue
        else:
            break
    
browser = webdriver.Chrome(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
for i in range(3):
    link = urls[i]
    for j in range(pages[i]):
        url = link.format(j+1)
        r = requests.get(url, headers=req_headers)
        soup= BeautifulSoup(r.text, "html.parser")
        movie_containers = soup.find_all('ul', class_ = 'photo-cards')    
        photos= soup.find_all('a', class_ = 'zsg-photo-card-overlay-link')    
        for photo in range(len(photos)):
            l= 'https://www.zillow.com' +photos[photo]['href'] + '?fullpage=true'
            browser.get(l)
            time.sleep(5)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            _pause_for_captcha(browser)
            try:
                myElem = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'listing-provided-by')))
                print("Page is ready!")
            except TimeoutException:
                print("Loading took too much time!")
            try:
                x= browser.find_element_by_xpath("//h1[@class='zsg-h1']")
                x = x.text.strip().replace("\n","")
            except:
                x= browser.find_element_by_xpath("//header[@class='zsg-content-header addr']")
                x = x.text.strip()
                num = x.rfind("\t")
                if(num == -1):
                    num = x.rfind("\n")
                x = x[:num].replace("\n", "")
            z = browser.find_element_by_xpath("//section[@id='listing-provided-by']")
            y = z.find_elements_by_css_selector("div")[1].text 
            num = y.rfind('(')
            y = y[num:]
            ser = pd.Series([x, y], index = ['Property Address', 'Owner Number'])
            profile = profile.append(ser, ignore_index=True)         
       
filename = 'output.xlsx'
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
profile.to_excel(writer, index=False)
writer.save()
