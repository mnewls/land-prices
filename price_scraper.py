# https://www.landsoftexas.com/Coryell-County-TX/all-land/

from multiprocessing.sharedctypes import Value
from unittest.mock import patch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd

# open each - grab date, job title, location - these will be different cols in the excel.
# 

from openpyxl import Workbook

import html5lib

from selenium.webdriver.support.ui import Select

# to find links
from bs4 import BeautifulSoup
import urllib.request

import time # to sleep

def get_page_info(driver, county):


    #https://www.landsoftexas.com/Coryell-County-TX/all-land/

    

    url_str = r'https://www.landsoftexas.com/' + county + '-County-TX/all-land/type-4031/sort-newest/'

    #print(url_str)

    driver.get(url_str)

    time.sleep(2)

    #print(driver.find_element_by_xpath("//*[@id='content']/div[1]/div[1]/div[1]/text()").getText())

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html5lib")

    price_list = soup.findAll("span", {"class": "_32f8d"})

    acreage_list = soup.findAll("span", {"class": "_1a278"})

    price_sum = []
    acreage_sum = []

    for price in price_list:

        #print(price.text)

        this_price = price.text
        #print(type(this_price))
        this_price = this_price.replace('$','')
        this_price = this_price.replace(',','')

        #print(this_price)

        price_sum.append(int(this_price))

        ##add code here to summ prices

    for acreage in acreage_list:

        this_acreage = acreage.text

        this_acreage = this_acreage.replace(' acres','')
        this_acreage = this_acreage.replace(',','')
        #this_price = this_price.replace(',','')
        #print(this_acreage)
        #print(int(this_acreage))

        acreage_sum.append(float(this_acreage))

        ##add code here to summ prices

    #print(soup.prettify())

    page_number_scrape = soup.findAll("span", {"class": "_8cfc9"})

    page_list = []

    for page in page_number_scrape:
        #print(page.text)
        page_list.append(page.text)

    final_page_len = len(page_list)

    for page_num in range(2, final_page_len+1):

        #print('looking at page: ' + str(page_num))

        url_str = r'https://www.landsoftexas.com/' + county + '-County-TX/all-land/type-4031/sort-newest/page-' + str(page_num) +'/'

        driver.get(url_str)

        time.sleep(2)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html5lib")

        #https://www.landsoftexas.com/Cass-County-TX/all-land/sort-newest/page-2/
        
        price_list = soup.findAll("span", {"class": "_32f8d"})

        acreage_list = soup.findAll("span", {"class": "_1a278"})

        for price in price_list:
            this_price = price.text
            #print(type(this_price))
            this_price = this_price.replace('$','')
            this_price = this_price.replace(',','')

            #print(this_price)

            price_sum.append(int(this_price))


        for acreage in acreage_list:
            this_acreage = acreage.text

            this_acreage = this_acreage.replace(' acres','')
            this_acreage = this_acreage.replace(',','')
            #this_price = this_price.replace(',','')
            #print(this_acreage)
            #print(int(this_acreage))

            acreage_sum.append(float(this_acreage))

    #for date in soup.findAll("div", {"class": "date"}):

    #print(price_sum[5])
    #print(acreage_sum[5])

    total_cost = sum(price_sum)

    total_acres = sum(acreage_sum)

    avg_PPA = total_cost / total_acres

    print("average cost per acre: " + str(avg_PPA))
           

def get_info():
    
    print('What county would you like to search:')

    county = input()

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(executable_path=r'C:\Users\Michael\Desktop\Python\Automate Application\chromedriver.exe', chrome_options=options)

    get_page_info(driver, county)
    


get_info()