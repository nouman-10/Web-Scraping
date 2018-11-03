from requests import get
from bs4 import BeautifulSoup as soup
import pandas as pd
import xlsxwriter
from urllib.request import urlopen as uReq
profile = pd.DataFrame(columns=['Company Name', 'Zip Code', 'Email', 'Website', 'Category'])
urls = []
mails = []
c = 'https://www.gelbeseiten.de/zimmervermietung'
response = get(c)
html_soup = soup(response.text, 'html.parser')
url = c + "/s{}"
response = get(url.format(1))
html_soup = soup(response.text, 'html.parser')
category = html_soup.find('input', {'class':'what_search'})['value']
con = html_soup.find('div', { "id" : "trefferlistenstatuszeile"})
if(con):
    con = con.find('p')
    if(con):
        con = con.text.strip()
        num = con.rfind(' ')
        con = int(con[num:])
        pages = (con//15) + 1
    else:
        pages = 1
for i in range(1, pages + 1):
    response = get(url.format(i))
    html_soup = soup(response.text, 'html.parser') 
    locality = html_soup.find_all('div', {'class':'table'})
    for x in locality:
        web = x.find('div', {'class':'website'})
        name = x.find(itemprop = "name")
        postalcode = x.find(itemprop = "postalCode")
        mail = x.find('a', {'class':'email_native_app'})
        if(mail):
            mail = mail['href']
            sindex = mail.find(":") + 1
            eindex = mail.find("?")
            email = mail[sindex:eindex]
            if(email in mails):
                continue
            mails.append(email)
            if(name):
                name = name.text
            else:
                name = 'N/A'
            if(postalcode):
                postalcode = postalcode.text
            else:
                postalcode = 'N/A'
            if(web):
                web = web.find('a', {'class' : 'link'})['href']
            else:
                web = 'N/A'
            print(email)
            ser = pd.Series([name, postalcode, email, web, category], index = ['Company Name', 'Zip Code', 'Email', 'Website', 'Category']) 
            profile = profile.append(ser, ignore_index=True)                       
print(profile)
filename = 'output.xlsx'
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
profile.to_excel(writer, index=False)
writer.save()  
            
    
