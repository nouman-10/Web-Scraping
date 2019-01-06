#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 12:18:43 2018

@author: nouman
"""

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
import xlsxwriter
profile = pd.DataFrame(columns=['Name', 'Price', 'Availability', 'Description', 'Detailed Part Description', 'Carrier Compatibilty', 'Model Compatibility', 'Warranty',
                                'SKU', 'Part Type', 'Compatible Model', 'Model Number', 'Manufacturer', 'Warranty', 'Part Number'])
url = 'https://www.mobiledefenders.com/apple.html?limit=all'
a = ['accessories']
flag = True
for i in a:
    if(flag):
        print(i)
        url = 'https://www.mobiledefenders.com/{}.html?limit=all'.format(i)
        uClient = uReq(url)
        pageHtml = uClient.read()
        uClient.close()
        pageSoup = soup(pageHtml, 'html.parser')
        containers = pageSoup.findAll('a', {"class" : "product-image"})
        print(len(containers))
        for i in containers:
            try:
                url = i['href']
                uClient = uReq(url)
                pageHtml = uClient.read()
                uClient.close()
                pageSoup = soup(pageHtml, 'html.parser')
                name_container = pageSoup.find('div', {"class" : "product-name"})
                name = name_container.h1.text.strip()
                price_container = pageSoup.find('span', {"class" : "price"})
                price = price_container.text.strip()
                if( pageSoup.find('p', {"class" : "availability in-stock"})):
                    avail_container =  pageSoup.find('p', {"class" : "availability in-stock"})
                    avail = avail_container.span.text.strip()
                else:
                    avail_container =  pageSoup.find('p', {"class" : "availability out-of-stock"})
                    avail = avail_container.span.text.strip()
                des_container = pageSoup.find('div', {"class" : "std"})
                des = des_container.findAll('p')
                l = len(des)
                if(l >= 1):
                    detail_desc = des[0].text.strip()
                else:
                    detail_desc = 'N/A'
                if(l >= 2):
                    detail_desc0 = des[1].text.strip()
                else:
                    detail_desc0 = 'N/A'
                if(l >= 3):
                    detail_desc1 = des[2].text.strip()
                else:
                    detail_desc1 = 'N/A'
                if(l >= 4):
                    detail_desc2 = des[3].text.strip()
                else:
                    detail_desc2 = 'N/A'
                if(l >= 5):
                    detail_desc3 = des[4].text.strip()
                else:
                    detail_desc3 = 'N/A'
                container = pageSoup.find('table', {"id" : "product-attribute-specs-table"})
                print(len(container))
                container = container.findAll('td')
                print(container)
                SKU = container[0].text.strip()
                part_type = container[1].text.strip()
                compatible_model = container[2].text.strip()
                model_number = container[3].text.strip()
                manufacturer = container[4].text.strip()
                warranty = container[5].text.strip()
                part_number = container[6].text.strip()
                print(name)
                print(price)
                print(avail)
                print(detail_desc)
                print(detail_desc0)
                print(detail_desc1)
                print(detail_desc2)
                print(detail_desc3)
                print(SKU)
                print(part_type)
                print(compatible_model)
                print(model_number)
                print(manufacturer)
                print(warranty)
                print(part_number)
                ser = pd.Series([name, price, avail, detail_desc, detail_desc0, detail_desc1, detail_desc2, detail_desc3, SKU, part_type, compatible_model, model_number, manufacturer,
                                 warranty, part_number], index = ['Name', 'Price', 'Availability', 'Description', 'Detailed Part Description', 'Carrier Compatibilty', 'Model Compatibility', 'Warranty',
                                            'SKU', 'Part Type', 'Compatible Model', 'Model Number', 'Manufacturer', 'Warranty', 'Part Number'])
                profile = profile.append(ser, ignore_index=True)
            except Exception as e:
                break
                flag = False
print(profile)
filename = 'free3.xlsx'
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
profile.to_excel(writer, index=False)
writer.save()
