#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 14:21:38 2024

@author: benleidig
"""

# imports
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# inputs
username = str(input('Enter username: '))
password = str(input('Enter password: '))
y_n = str(input('Production margins; all the same? (y/n): ')).lower()

if y_n == 'y':
    production_margin = int(input('Enter production margin: '))
    traditional_production_margin = production_margin
    low_end_production_margin = production_margin
    high_end_production_margin = production_margin
    performance_production_margin = production_margin
    size_production_margin = production_margin
else:
    traditional_production_margin = int(input('Enter traditional production margin: '))
    low_end_production_margin = int(input('Enter low-end production margin: '))
    high_end_production_margin = int(input('Enter high-end production margin: '))
    performance_production_margin = int(input('Enter performance production margin: '))
    size_production_margin = int(input('Enter size production margin: '))
                                 
wait_time = int(input('Enter wait time (sec; at least 3 is recommended): '))
## chrome_driver_path = str(input('Enter Chrome Driver path: '))
chrome_driver_path = '/Users/benleidig/Downloads/chromedriver-mac-arm64/chromedriver'
## browser_path = str(input('Enter browser path: '))
browser_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"

# navigation steps
courier_navigation = ['/html/body/div[2]/div/div/main/div[1]/form/div[3]/button',
                      '/html/body/div[1]/div/main/div/div/div[5]/a',
                      '/html/body/nav/div/div[2]/ul/li[4]/a',
                      '/html/body/nav/div/div[2]/ul/li[4]/ul/li[2]/a',
                      '/html/body/div[3]/div/div/div/div/div[1]/table/tbody/tr/td[2]/a'
                      ]

# market info dataframe
df = pd.DataFrame({'market':['traditional', 'low-end', 'high-end', 'performance', 'size'],
                   'market-size':[0, 0, 0, 0, 0],
                   'demand-growth-rate':[0, 0, 0, 0, 0],
                   'potential-market-share':[0, 0, 0, 0, 0],
                   'product-satisfaction':[0, 0, 0, 0, 0],
                   'segment-satisfaction':[0, 0, 0, 0, 0],
                   'last-year-units-sold':[0, 0, 0, 0, 0],
                   'leftover-inventory': [0, 0, 0, 0, 0],
                   'production-margin': [traditional_production_margin, low_end_production_margin, high_end_production_margin, performance_production_margin, size_production_margin],
                   'marketing-forecast': [0, 0, 0, 0, 0],
                   'production-forecast': [0, 0, 0, 0, 0]
                   })

# configurations
options = Options()
options.binary_location = browser_path
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# retrieving url and inputting username and password
driver.get('https://ww2.capsim.com/login/')
username_field = driver.find_element(By.ID, 'username')
username_field.send_keys(username)
password_field = driver.find_element(By.ID, 'password')
password_field.send_keys(password)

# navigating to courier report
for step in courier_navigation:
    
    if step == '/html/body/div[3]/div/div/div/div/div[1]/table/tbody/tr/td[2]/a':
        button = driver.find_element(By.XPATH, step)
        button.click()
        time.sleep(wait_time)
        tabs = driver.window_handles
        driver.switch_to.window(tabs[-1])
        
    else:
        button = driver.find_element(By.XPATH, step)
        button.click()
        time.sleep(wait_time)
        

