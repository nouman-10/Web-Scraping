import pandas as pd
from selenium import webdriver
import xlsxwriter
from selenium.webdriver.chrome.options import Options
chrome_options = Options()  
chrome_options.add_argument("--headless")  
profile = pd.DataFrame(columns=['Name', 'Position', 'Email'])
url = 'https://isearch.asu.edu/asu-people/q=Professor&start={}'
browser = webdriver.Chrome(options=chrome_options)

for i in range(1, 3010, 10):
    print(i)
    myUrl = url.format(i)
    browser.get(myUrl)
    even = browser.find_elements_by_xpath("//div[@class='row row-header asu_directory_people_row asu_people_row_even']")
    odd = browser.find_elements_by_xpath("//div[@class='row row-header asu_directory_people_row asu_people_row_odd']")
    total = even + odd
    for person in total:
        try:
            jobTitle = person.find_element_by_class_name('job-title')
            dept = person.find_element_by_class_name('dept')
            Postion = jobTitle.text + ' ' + dept.text
            mail = person.find_element_by_class_name('emailAddress')
            name = person.find_element_by_class_name('displayName')
            ser = pd.Series([name.text, Postion, mail.text], index = ['Name', 'Position', 'Email'])
            profile = profile.append(ser, ignore_index=True)
        except:
            continue

filename = 'output.xlsx'
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
profile.to_excel(writer, index=False)
writer.save()

