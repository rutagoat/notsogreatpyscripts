from selenium import webdriver
import requests, csv
from bs4 import BeautifulSoup

#uses selenium because of cloudflare ddos protection on website when trying to visit for first time

browser = webdriver.Chrome(executable_path=r'chromedriver.exe') 

url = 'https://1337x.to/user/bookrar/'
url = url.replace('user/'+url.split('/')[4], url.split('/')[4]+'-torrents/1')

browser.get(url)

lastPage = int(browser.find_element_by_xpath('/html/body/main/div/div/div[3]/div[2]/ul/li[9]/a').get_attribute('href').split('/')[4])

def source(text):
    #tableData = text.find_element_by_tag_name('tbody')
    rowsData = text.find_elements_by_tag_name('tr')
    rowsLen = len(rowsData)

    return rowsData, rowsLen


scrapedata = []

for pageno in range(2,lastPage+1):
    
    data, lines = source(browser)
    
    for row in range(1,int(lines)):
        info = data[row].find_elements_by_tag_name('td')
        filename = info[0].text
        seeders = info[1].text
        leechers = info[2].text
        size = info[3].text
        uploadTime = info[4].text
        filelink = info[0].find_elements_by_tag_name('a')[1].get_attribute('href')
        torrentid = filelink.split('/')[4]
        getPage = requests.get(filelink)
        soup = BeautifulSoup(getPage.content,'html.parser')
        magnetlink = soup.select('a[href^="magnet"]')[0]['href']
        
        scrapedata.append({'Torrentid' : torrentid, 'Name': filename, 'Seeders': seeders, 'Leechers': leechers, 'Size': size, 'Time': uploadTime, 'Link': filelink, 'MagnetLink': magnetlink})

        #print(filename + ' - ' + seeders + ' - ' + leechers + ' - ' + size + ' - ' + uploadTime + ' - ' + filelink + ' - ' + magnetlink)
        
    newUrl = url.replace('1/',str(pageno)+'/')
    browser.get(newUrl)

with open(url.split('/')[3]+'.csv', mode='w') as csv_file:
    fieldnames = ['Torrentid','Name', 'Seeders', 'Leechers', 'Size', 'Time', 'Link', 'MagnetLink']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for onekey in range(len(scrapedata)):
        writer.writerow(scrapedata[onekey])

        
