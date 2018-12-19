from fake_useragent import UserAgent
import pandas as pd
import xlsxwriter
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

def get_proxies():
    driver = webdriver.Chrome()
    driver.get("https://free-proxy-list.net/")
    time.sleep(10)
    PROXIES = []
    proxies = driver.find_elements_by_css_selector("tr[role='row']")
    for p in proxies:
        result = p.text.split(" ")
        PROXIES.append(result[0]+":"+result[1])

    driver.close()
    return PROXIES

ALL_PROXIES = get_proxies()

def proxy_driver():
    global ALL_PROXIES

    if (len(ALL_PROXIES) > 0):
        pxy = ALL_PROXIES[-1]
    else:
        while(len(ALL_PROXIES) == 0):
            print("--- Proxies used up (%s)" % len(ALL_PROXIES))
            ALL_PROXIES = get_proxies()
            return webdriver.Firefox()
        pxy = ALL_PROXIES[-1]

    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')
    service_args = [
            '--proxy={0}'.format(pxy),
            '--proxy-type=http'
        ]

    driver = webdriver.Chrome(options = options, service_args = service_args)
    print('Switched to proxy: {}'.format(pxy))
    return driver

browser = proxy_driver()
print(ALL_PROXIES)
profile1 = pd.DataFrame(columns=['Price', 'Description'])
profile2 = pd.DataFrame(columns=['Price', 'Description'])
profile3 = pd.DataFrame(columns=['Price', 'Description'])
profile4 = pd.DataFrame(columns=['Price', 'Description'])
profile5 = pd.DataFrame(columns=['Price', 'Description'])
profile6 = pd.DataFrame(columns=['Price', 'Description'])
profile7 = pd.DataFrame(columns=['Price', 'Description'])
profile8 = pd.DataFrame(columns=['Price', 'Description'])
profile9 = pd.DataFrame(columns=['Price', 'Description'])
profile10 = pd.DataFrame(columns=['Price', 'Description'])

for i in range(1,101):
    image = pd.DataFrame(columns=['Image Url {}'.format(i)])
    profile1 = profile1.join(image)
    profile2 = profile2.join(image)
    profile3 = profile3.join(image)
    profile4 = profile4.join(image)
    profile5 = profile5.join(image)
    profile6 = profile6.join(image)
    profile7 = profile7.join(image)
    profile8 = profile8.join(image)
    profile9 = profile9.join(image)
    profile10 = profile10.join(image)


url = "https://www.rvtrader.com/RVs/rvs-for-sale?zip=78640&radius=150&sort=distance%3Aasc&page={}"
browser.implicitly_wait(30)
browser.get(url.format(1))
x= browser.find_element_by_xpath("//div[@class='listingsTitle customPageInfo']")
total = x.find_element_by_tag_name('b').text.strip()
total = int(total.replace(',',''))
count = 0
count1 = 0
print('Scraping Started...')
for i in range(1, (total//25) + 1):
        if(i%10 == 0):
            count = 0
        while(True):
            print('Starting to scrape page number: {}'.format(i))
            links = []
            browser.get(url.format(i))
            x = browser.find_elements_by_xpath("//div[@class='listing-info-top padding10 padding-top0']")
            if(len(x) > 0):    
                for a in x:
                        link = a.find_element_by_tag_name('a').get_attribute("href")
                        links.append(link)
                break
            else:
                browser.quit()
                new = ALL_PROXIES.pop()
                print('Proxy Blocked {}'.format(new))
                browser = proxy_driver()
                continue
        for num in range(len(links)):
            while(True):
                try:
                    browser.get(links[num])
                    time.sleep(2)
                    try:
                            price = browser.find_element_by_xpath("//div[@class='detail-price bold']").text.strip()
                    except:
                            price = ""
                    desc = browser.find_element_by_xpath("//div[@class='printSellerInfo']").text.replace('\n', '')
                    desc = desc.replace('Description & Comments', 'Description & Comments\n')

                    images = browser.find_elements_by_xpath("//img[@class='rsTmb']")
                    imgs = [price, desc]
                    img = ''
                    for image in images[:100]:
                            img = image.get_attribute("src")
                            img = img[:img.find('?')]
                            imgs.append(img)
                    while(len(imgs) != 102):
                            imgs.append('')
                    if(i <= 10):
                        print('Products Scraped {}'.format(count1))
                        profile1.loc[count] = imgs
                    elif(i > 10 and i <= 20 ):
                        print('Products Scraped {}'.format(count1))
                        print(profile1)
                        profile2.loc[count] = imgs
                    elif(i > 20 and i <= 30 ):
                        print('Products Scraped {}'.format(count1))
                        print(profile2)
                        profile3.loc[count] = imgs
                    elif(i > 30 and i <= 40 ):
                        print('Products Scraped {}'.format(count1))
                        print(profile3)
                        profile4.loc[count] = imgs
                    elif(i > 40 and i <= 50 ):
                        print('Products Scraped {}'.format(count1))
                        print(profile4)
                        profile5.loc[count] = imgs
                    elif(i > 50 and i <= 60 ):
                        print('Products Scraped {}'.format(count1))
                        print(profile5)
                        profile6.loc[count] = imgs
                    elif(i > 60 and i <= 70 ):
                        print('Products Scraped {}'.format(count1))
                        print(profile6)
                        profile7.loc[count] = imgs
                    elif(i > 70 and i <= 80 ):
                        print('Products Scraped {}'.format(count1))
                        print(profile7)
                        profile8.loc[count] = imgs
                    elif(i > 80 and i <= 90 ):
                        print('Products Scraped {}'.format(count1))
                        print(profile8)
                        profile9.loc[count] = imgs
                    elif(i > 90 and i <= 100 ):
                        print('Products Scraped {}'.format(count1))
                        print(profile9)
                        profile10.loc[count] = imgs
                    count += 1
                    count1 += 1
                    del imgs, img, images, price, desc
                    
                    
                    break
                except:
                    browser.quit()
                    new = ALL_PROXIES.pop()
                    print('Proxy Blocked {}'.format(new))
                    browser = proxy_driver()
                    continue
print(profile10)
frames = [profile1, profile2, profile3, profile4, profile5, profile6, profile7, profile8, profile9, profile10]
profile = pd.concat(frames)
filename = 'output.xlsx'
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
profile.to_excel(writer, index=False)
writer.save()  
