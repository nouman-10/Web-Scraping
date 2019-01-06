from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd
import xlsxwriter
from selenium import webdriver
import time

browser = webdriver.Firefox(executable_path='/usr/local/geckodriver')
myUrl = "http://www.miraclehunter.com/marian_apparitions/unapproved_apparitions/index.html"
browser.get(myUrl)
pageSoup = soup(browser.page_source, 'html.parser')

containers = pageSoup.findAll('table')[8]

tr = containers.findAll('tr')
containers2 = pageSoup.findAll('div', {"class" : "container row form1 striped"})
for i in containers2:
    containers.append(i)
profile = pd.DataFrame(columns=['Record', 'Name', 'Telephone', 'State', 'ZipCode', 'License #', 'Website', 'Facebook', 'LinkedIn', 'Yelp', 'About Me', 'Employee 1',
'Employee 1 license', 'Employee 2', 'Employee 2 license', 'Employee 3', 'Employee 3 license', 'Employee 4', 'Employee 4 license', 'Employee 5', 'Employee 5 license'])
count = 1
for i in containers:
    website_container = i.find('li', {'class': 'visitSite'})
    website = website_container.a['href']
    client = uReq(website)
    page = client.read()
    client.close()
    pgSoup = soup(page, 'html.parser')
    try:
        name_container = pgSoup.find('h1', {'id': 'AgentNameLabelId'})
        name_container = name_container.find('span', {'itemprop': 'name'})
        name =  name_container.text.strip()
    except:
        name_container = pgSoup.find('h2', {'id': 'AgentNameLabelId'})
        name_container = name_container.find('span', {'itemprop': 'name'})
        name =  name_container.text.strip()
    phone_container = pgSoup.find('span', {'id': 'offNumber_tab_mainLocContent_0'})
    phone = phone_container.span.text.strip()
    address_container = pgSoup.find('span', {'id': 'locStreetContent_mainLocContent'})
    address = address_container.text.strip()
    state_container = pgSoup.find('span', {'itemprop': 'addressRegion'})
    state = state_container.text.strip()
    zip_container = pgSoup.find('span', {'itemprop': 'postalCode'})
    zipCode = zip_container.text.strip()
    license_container = pgSoup.find('span', {'class': 'sfx-text thirteenPixel-fontSize zeroMargingSpace licenseText'})
    licence = license_container.text.strip()
    lic = licence[licence.find(':')+2:]
    employees = ['NA', 'NA', 'NA', 'NA', 'NA']
    employeesLicenses = ['NA', 'NA', 'NA', 'NA', 'NA']
    for j in range(5):
        try:
            employees_container = pgSoup.find('h6', {'id': 'teamMember_{}'.format(j)})
            employees[j] = employees_container.text.strip()
            employeesLic_container = pgSoup.find('span', {'id': 'teamMemberLicenseNumber_{}'.format(j)})
            empLic = employeesLic_container.text.strip()
            empLic = ''.join(empLic.split())
            employeesLicenses[j] = empLic
        except Exception as e:
            if(employees[j] == employeesLicenses[j]):
                break
            else:
                employees[j] = 'NA'
                break
    print("DETAILS OF EMPLOYEE {}".format(count))
    print('Name: {}'.format(name))
    print('Phone Number: {}'.format(phone))
    print('Address: {}'.format(address))
    print('State: {}'.format(state))
    print('Postal Code: '.format(zipCode))
    print('License Number: {}'.format(lic))
    try:
        webs_container = pgSoup.find('a', {'id': 'agentlink_mainLocContent_0'})
        webs = webs_container.get('href')
        print('Website: {}'.format(webs))
    except:
        webs = 'NA'
    try:
        facebook_container = pgSoup.find('a', {'id': 'socialButton_phone_Facebook'})
        facebook = facebook_container.get('href')
        print('Facebook: {}'.format(facebook))
    except:
        facebook = 'NA'
    try:
        linked_container = pgSoup.find('a', {'id': 'socialButton_phone_LinkedIn'})
        linkedIn = linked_container.get('href')
        print('LinkedIn: {}'.format(linkedIn))
    except:
        linkedIn = 'NA'
    try:
        yelp_container = pgSoup.find('a', {'id': 'socialButton_phone_Yelp'})
        yelp = yelp_container.get('href')
        print('Yelp: {}'.format(yelp))
    except:
        yelp = 'NA'
    try:
        aboutMe_container = pgSoup.find('div', {'id': 'aboutMeContent'})
        aboutMe = aboutMe_container.text.strip()
        print('About Me: {}'.format(aboutMe))
    except:
        aboutMe = 'NA'
    
    for k in range(len(employees)):
        print('Employee No. {}:'.format(k+1))
        print('Name: {}'.format(employees[k]))
        print('License: {}'.format(employeesLicenses[k]))
    ser = pd.Series([count, name, phone, state, zipCode, lic, webs, facebook, linkedIn, yelp, aboutMe, employees[0], employeesLicenses[0], employees[1], employeesLicenses[1],
                     employees[2], employeesLicenses[2], employees[3], employeesLicenses[3], employees[4], employeesLicenses[4]], index = ['Record', 'Name', 'Telephone',
                    'State', 'ZipCode', 'License #', 'Website', 'Facebook', 'LinkedIn', 'Yelp', 'About Me', 'Employee 1', 'Employee 1 license', 'Employee 2',
                    'Employee 2 license', 'Employee 3', 'Employee 3 license', 'Employee 4', 'Employee 4 license', 'Employee 5', 'Employee 5 license']) 
    profile = profile.append(ser, ignore_index=True)
    count += 1
print(profile)
filename = 'profile.xlsx'
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
profile.to_excel(writer, index=False)
writer.save()
