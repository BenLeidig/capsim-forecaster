#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 14:21:38 2024

@author: benleidig
"""

# imports
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# creating empty lists
products = []

# navigation steps
courier_navigation = ['/html/body/div[2]/div/div/main/div[1]/form/div[3]/button',
                      '/html/body/div[1]/div/main/div/div/div[5]/a',
                      '/html/body/nav/div/div[2]/ul/li[4]/a',
                      '/html/body/nav/div/div[2]/ul/li[4]/ul/li[2]/a',
                      '/html/body/div[3]/div/div/div/div/div[1]/table/tbody/tr/td[2]/a'
                      ]

# function definitions
def find_market_size(num):
    market_size_element = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div/div[{num}]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/table/tbody/tr[1]/td[2]')
    market_size = int(market_size_element.text.replace(',', '').replace(' ', ''))
    return market_size

def find_demand_growth_rate(num):
    demand_growth_rate_element = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div/div[{num}]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/table/tbody/tr[4]/td[2]')
    demand_growth_rate = float(demand_growth_rate_element.text.replace('%', '').replace('.', '').replace(' ', ''))*0.001
    return demand_growth_rate

def find_potential_market_share(num):
    try:
        tr_xpath = '/html/body/div/div/div/div/div[10]/div/div[3]/div[2]/div/table/tbody/tr'
        rows = driver.find_elements(By.XPATH, tr_xpath)
        target_product = products[num]
        for row in rows:
            product_td = row.find_element(By.XPATH, 'td[1]')
            product = product_td.text
            if product == target_product:
                value_td = row.find_element(By.XPATH, f'td[{num + 2}]')
                value = value_td.text
                potential_market_share = float(value.replace('%', '').replace('.', '').replace(' ', ''))*0.001
                return potential_market_share
    except Exception as e:
        print(f'Error processing product values for {target_product}: {e}')
        return None

def find_product_satisfaction(num):
    try:
        tr_xpath = f'/html/body/div[1]/div/div/div/div[{num}]/div/div[1]/div[2]/div[3]/table/tbody/tr'
        rows = driver.find_elements(By.XPATH, tr_xpath)
        for row in rows:
            product_td = row.find_element(By.XPATH, 'td[1]')
            product = product_td.text
            if product in products:
                value_td = row.find_element(By.XPATH, 'td[15]')
                product_satisfaction = value_td.text.replace(' ', '')
                return int(product_satisfaction)
    except Exception as e:
        print(f'Error processing div[{num}]: {e}')
        
def find_segment_satisfaction(num):
    try:
        sum_td_15 = 0
        tr_xpath = f'/html/body/div[1]/div/div/div/div[{num}]/div/div[1]/div[2]/div[3]/table/tbody/tr'
        rows = driver.find_elements(By.XPATH, tr_xpath)
        for row in rows:
            try:
                td_15 = row.find_element(By.XPATH, 'td[15]')
                sum_td_15 += int(td_15.text.replace(' ', ''))
            except Exception as e:
                print(f"Error accessing td[15] in div[{num}]: {e}")
        return sum_td_15
    except Exception as e:
        print(f'Error processing div[{num}]: {e}')

# inputs
username = str(input('Enter username: '))
password = str(input('Enter password: '))
products.append(str(input('Enter traditional product name: ')))
products.append(str(input('Enter low-end product name: ')))
products.append(str(input('Enter high-end product name: ')))
products.append(str(input('Enter performance product name: ')))
products.append(str(input('Enter size product name: ')))
y_n = str(input('Production margins; all the same? (y/n): ')).lower()

if y_n == 'y':
    production_margin = float(input('Enter production margin: '))
    traditional_production_margin = production_margin
    low_end_production_margin = production_margin
    high_end_production_margin = production_margin
    performance_production_margin = production_margin
    size_production_margin = production_margin
else:
    traditional_production_margin = float(input('Enter traditional production margin: '))
    low_end_production_margin = float(input('Enter low-end production margin: '))
    high_end_production_margin = float(input('Enter high-end production margin: '))
    performance_production_margin = float(input('Enter performance production margin: '))
    size_production_margin = float(input('Enter size production margin: '))
                                 
wait_time = int(input('Enter step wait time (sec; at least 3 is recommended): '))
#### chrome_driver_path = str(input('Enter Chrome Driver path: '))
chrome_driver_path = '/Users/benleidig/Downloads/chromedriver-mac-arm64/chromedriver'
#### browser_path = str(input('Enter browser path: '))
browser_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"

print('Processing...')
time.sleep(1)

# market info dataframe
df = pd.DataFrame({'market':['traditional', 'low-end', 'high-end', 'performance', 'size'],
                   'market-size':[0, 0, 0, 0, 0],
                   'demand-growth-rate':[0.0, 0.0, 0.0, 0.0, 0.0],
                   'potential-market-share':[0.0, 0.0, 0.0, 0.0, 0.0],
                   'product-satisfaction':[0, 0, 0, 0, 0],
                   'segment-satisfaction':[0, 0, 0, 0, 0],
                   'last-year-units-sold':[0, 0, 0, 0, 0],
                   'leftover-inventory': [0, 0, 0, 0, 0],
                   'production-margin': [traditional_production_margin, low_end_production_margin, high_end_production_margin, performance_production_margin, size_production_margin],
                   'marketing-forecast': [0.0, 0.0, 0.0, 0.0, 0.0],
                   'production-forecast': [0.0, 0.0, 0.0, 0.0, 0.0]
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
        time.sleep(wait_time+3)
        tabs = driver.window_handles
        driver.switch_to.window(tabs[-1])
        
    else:
        button = driver.find_element(By.XPATH, step)
        button.click()
        time.sleep(wait_time)
        
# inputting market size
for i in range(0, 5):
    df.iloc[i, 1] = find_market_size(i+5)
    
# inputting demand growth rate
for i in range(0, 5):
    df.iloc[i, 2] = find_demand_growth_rate(i+5)
    
# inputting potential market share
for i in range(0, 5):
    df.iloc[i, 3] = find_potential_market_share(i)

# inputting product satisfaction
for i in range(0, 5):
    df.iloc[i, 4] = find_product_satisfaction(i+5)
    
# inputting segment satisfaction
for i in range(0, 5):
    df.iloc[i, 5] = find_segment_satisfaction(i+5)
    
print(df[['market-size', 'demand-growth-rate', 'potential-market-share', 'product-satisfaction', 'segment-satisfaction']])
