#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base64 import b64encode
import mechanize
from bs4 import BeautifulSoup as soup
import pandas as pd
import xlsxwriter
import openpyxl

url = 'https://retailer.partykungen.se/bartillbehor/'
username = 'abcd'
password = '****'

# I have had to add a carriage return ('%s:%s\n'), but
# you may not have to.
b64login = b64encode('%s:%s' % (username, password))

br = mechanize.Browser()

# # I needed to change to Mozilla for mine, but most do not
# br.addheaders= [('User-agent', 'Mozilla/5.0')]

br.addheaders.append( 
  ('Authorization', 'Basic %s' % b64login )
)

profile = pd.DataFrame(columns=['Start URL', 'Title', 'Comments',
            'Price', 'Description', 'Tags', 'Img Main', 'Article No.', 'Stock'])

br.open(url1)
r = br.response()
data = r.read()
pageSoup = soup(data, 'html.parser')
b = pageSoup.findAll('div',  {'class': 'two columns menu-item tight'})
url2 = url1 + b[5].find('a').get('href')
br.open(url2)
r = br.response()
data = r.read()
pageSoup = soup(data, 'html.parser')
b = pageSoup.find('span',  {'class': 'hits'})
q = int(b.text.strip())//30 + 1
for i in range(1,q+1):
    url = url2 + str(i) + '/'
    br.open(url)
    r = br.response()
    data = r.read()
    pageSoup = soup(data, 'html.parser')
    b = pageSoup.findAll('div',  {'class': 'columns white three product '})
    for s in b:
      count += 1
      link_container = s.find_all('a')
      link = 'https://retailer.partykungen.se' + link_container[1].get('href')
      br.open(link)
      r1 = br.response()
      data1 = r1.read()
      page = soup(data1, 'html.parser')
      if(page.find('div', {'class': 'comments-count'})):
        com_container = page.find('div', {'class': 'comments-count'})
        comments = com_container.text.strip()
      else:
        comments = '(0 omdömen)'
      if(page.find('span', {'class': 'sale-price'})):
        price_container = page.find('span', {'class': 'sale-price'})
        price = price_container.text.strip()
      else:
        price_container = page.find('div', {'class': 'price product-minprice'})
        price = price_container.text.strip()
      desc_container = page.find('div', {'class': 'product-description'})
      description =desc_container.text.strip()
      tags_container = page.find('ul', {'class': 'product-tags'})
      tags = tags_container.find_all('li')
      tag = ''
      for l in tags:
        tag = tag + l.text.strip() + ' '
      name_container1 = page.findAll('div', {'class' :'columns nine product-variant-name'})
      price_container1 = page.findAll('div',{'class' :'columns three product-variant-price'})
      article_container = page.findAll('div', {'class':'artnr'})
      stock_container =  page.findAll('div', {'class':'columns six product-variant-stock'})
      image_container1 = page.findAll('div', {'class' :'columns eleven product-variant-image'})
      
      for c in range(len(name_container1)):
          name1 = name + name_container1[c].text.strip()
          if(price_container1[c].find('span', {'class': 'sale-price'})):
              price_container = price_container1[c].find('span', {'class': 'sale-price'})
              price = price_container.text.strip()
          else:
              price_container = price_container1[c].find('div', {'class': 'price'})
              price = price_container.text.strip()
          image = image_container1[c]['style']
          image = url1 + image[image.find('.net/') + 6:] 
          art = ' '.join(article_container[c].text.strip().split())
          stock = stock_container[c].text.strip()
          
          ser = pd.Series([link, name1, comments, price, description, tag, image, art, stock], 		  index = ['Start URL', 'Title', 'Comments',
            'Price', 'Description', 'Tags', 'Img Main', 'Article No.', 'Stock']) 
          profile = profile.append(ser, ignore_index=True)
   
print(profile)
filename = 'excel.xlsx'
writer = pd.ExcelWriter(filename, engine='openpyxl')
profile.to_excel(writer, sheet_name = 'Sheet1')
writer.save()
