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

    

    url_str = r'https://www.landsoftexas.com/' +county+ '-County-TX/all-land/no-house/type-4031/sort-newest/'

    #https://www.landsoftexas.com/zip-75555/all-land/

    #print(url_str)

    driver.get(url_str)

    time.sleep(2)

    #print(driver.find_element_by_xpath("//*[@id='content']/div[1]/div[1]/div[1]/text()").getText())

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html5lib")

    price_list = soup.findAll("div", {"class": "_12a2b"})

    #print(price_list)
    #test_text = price_list[1].text

    #test_filter = test_text[test_text.find(start:='>')+len(start):test_text.find('<')]

    #print(test_filter)

    
    #print(test_break)

    #acreage_list = soup.findAll("span", {"class": "_1a278"})

    

    price_sum = []
    acreage_sum = []

    for price in price_list:

        #print(price.text)

        this_price = price.text

        filter = this_price[this_price.find(start:='>')+len(start):this_price.find('<')]

        break_up_data = filter.split(' ')

        #print(break_up_data)

        acres = break_up_data[0]

        trigger_no_data = False

        try: 
            extracted_cost = break_up_data[3]
        except:
            print(break_up_data)
            trigger_no_data = True


        extracted_cost = extracted_cost.replace('$','')
        extracted_cost = extracted_cost.replace(',','')
        extracted_cost = extracted_cost.ljust(1 + len(extracted_cost), '0')


        #print(acres)
        #print(extracted_cost)

        #print(type(this_price))
        

        #print(this_price)
        if trigger_no_data == False:
            price_sum.append(int(extracted_cost))
            acreage_sum.append(int(float(acres)))
        else:
            print('there was a listing with no price')

        trigger_no_data = False
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

        url_str = r'https://www.landsoftexas.com/' +county+ '-County-TX//all-land/no-house/type-4031/sort-newest/'

        driver.get(url_str)

        time.sleep(2)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html5lib")
        ###

        """
        there may be a way to make this whole thing work with: https://www.landsofamerica.com/Indiana/all-land/

        for alternate states, etc

        
        """

        #https://www.landsoftexas.com/Cass-County-TX/all-land/sort-newest/page-2/
        
        price_list = soup.findAll("div", {"class": "_12a2b"})


        for price in price_list:
            this_price = price.text

            filter = this_price[this_price.find(start:='>')+len(start):this_price.find('<')]

            break_up_data = filter.split(' ')

            #print(break_up_data)

            acres = break_up_data[0]

            trigger_no_data = False

            try: 
                extracted_cost = break_up_data[3]
            except:
                #print(break_up_data)
                trigger_no_data = True

            extracted_cost = extracted_cost.replace('$','')
            extracted_cost = extracted_cost.replace(',','')
            extracted_cost = extracted_cost.ljust(1 + len(extracted_cost), '0')


            #print(acres)
            #print(extracted_cost)

            #print(type(this_price))
            

            #print(this_price)

            if trigger_no_data == False:
                price_sum.append(int(extracted_cost))
                acreage_sum.append(int(float(acres)))
            else:
                print('there was a listing with no price')

            trigger_no_data = False


        
    #for date in soup.findAll("div", {"class": "date"}):

    #print(sum(price_sum))
    #print(sum(acreage_sum))

    total_cost = sum(price_sum)

    total_acres = sum(acreage_sum)

    avg_PPA = total_cost / total_acres

    print("average cost per acre in county " + county + " is: $" + str(avg_PPA))
           

def get_info():
    
    print('What county would you like to search:')

    county = input()

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(executable_path=r'C:\Users\Michael\Desktop\Python\Automate Application\chromedriver.exe', chrome_options=options)

    get_page_info(driver, county)
    


get_info()