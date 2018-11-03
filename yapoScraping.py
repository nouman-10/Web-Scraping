#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 17:00:00 2018

"""

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
import xlsxwriter
import urllib.request
from selenium import webdriver
import time

profile = pd.DataFrame(columns=['Link', 'Descripción de ubicación la propiedad', 'Descripción', 'Código', 
                    'Tipo de inmueble', 'Valor en $ (Pesos)', 'Valor en UF', 'Fecha de publicación', 'Dormitorios',
                    'Baños', 'Nombre contacto', 'Comuna', 'Superficie total', 'Superficie útil', 'Contacto URL'])

browser = webdriver.Chrome()
myUrl = 'https://www.yapo.cl/region_metropolitana/comprar?ca=15_s&l=0&w=1&cmn=%20&%20cmn%20=%20301%20&%20ret%20=%201'
browser.get(myUrl)
pageSoup = soup(browser.page_source, 'html.parser')

pages = pageSoup.find('span',  {'class', 'nohistory FloatRight'}).a['href']

index = pages.rfind('=')

lastPage = int(pages[index+1:])

pages = pages[:index+1]

for i in range(lastPage):
    url = pages + str(i+1)
    browser.get(url)
    pageSoup = soup(browser.page_source, 'html.parser')
    links = pageSoup.findAll('td', {'class' : 'thumbs_subject'})
    for link in links:
        h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13 = 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
        browser.get('https://www.yapo.cl/region_metropolitana/comprar/hermoso_departamento_en_la_cisterna_53703737.htm?ca=15_s&oa=53703737&xsp=12')
        pageSoup = soup(browser.page_source, 'html.parser')
        if(pageSoup.find('h1', {"id" : "da_subject"})):
            h1 = pageSoup.find('h1', {"id" : "da_subject"}).text.strip()
            
        if(pageSoup.find('small', {"class" : "date"})):
            h2 = pageSoup.find('small', {"class" : "date"}).text.strip().replace(u'\n', u' ').replace(u'\t', u'')
        
        if(pageSoup.find('h3', {"class" : "name"})):
            h3 = pageSoup.find('h3', {"class" : "name"}).text.strip()
        
        if(pageSoup.find('div', {"class" : "referencial-price text-right"})):
            h4 = pageSoup.find('div', {"class" : "referencial-price text-right"}).text.strip().replace(u'\n', u' ').replace(u'\t', u'')
        
        if(pageSoup.find('div', {"class" : "price text-right"})):
            h5 = pageSoup.find('div', {"class" : "price text-right"}).text.strip().replace(u'\n', u' ').replace(u'\t', u'')
        
        table = pageSoup.find('table')
        
        tr = table.findAll('tr')
        t = {}
        for k in tr:
            if(k.th and k.td):
                t[k.th.text.strip()] = k.td.text.strip()
        
        if 'Tipo de inmueble' in t.keys():
            h6 = t['Tipo de inmueble']
            
        if 'Comuna' in t.keys():
            h7 = t['Comuna']
            
        if 'Superficie total' in t.keys():
            h8 = t['Superficie total']
            
        if 'Superficie útil' in t.keys():
            h9 = t['Superficie útil']
            
        if 'Dormitorios' in t.keys():
            h10 = t['Dormitorios']
            
        if 'Baños' in t.keys():
            h11 = t['Baños']
            
        if 'Código' in t.keys():
            h12 = t['Código']
            
        if(pageSoup.find('div', {"class" : "description"})):
            h13 = pageSoup.find('div', {"class" : "description"}).text.strip().replace(u'\n', u' ')
            
        if(pageSoup.find('div', {'class':'phoneUser'})):
            h14_text = pageSoup.find('div', {'class':'phoneUser'})
            if(h14_text.img):
                h14 = 'yapo.cl' + h14_text.img['src']
        
        ser = pd.Series([link.a['href'], h1, h13 , h12, h6, h4, h5, h2, h10, h11, h3, h7, h8, h9, h14],
                        index =['Link', 'Descripción de ubicación la propiedad', 'Descripción', 'Código', 
                        'Tipo de inmueble', 'Valor en $ (Pesos)', 'Valor en UF', 'Fecha de publicación', 'Dormitorios',
                        'Baños', 'Nombre contacto', 'Comuna', 'Superficie total', 'Superficie útil', 'Contacto URL'])
        profile = profile.append(ser, ignore_index=True)
        print('done')

print(profile)
filename = 'fre.xlsx'
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
profile.to_excel(writer, index=False)
writer.save()
