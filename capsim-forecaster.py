#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 14:21:38 2024

@author: benleidig
"""

# imports
import os
import time
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

# creating empty lists
products = []

# navigation steps
courier_navigation = ['/html/body/div[2]/div/div/main/div[1]/form/div[3]/button',
                      '/html/body/div[1]/div/main/div/div/div[5]/a',
                      '/html/body/nav/div/div[2]/ul/li[4]/a',
                      '/html/body/nav/div/div[2]/ul/li[4]/ul/li[2]/a'
                      ]

# dataframe set up
df = pd.DataFrame({'market':['traditional', 'low-end', 'high-end', 'performance', 'size'],
                   'market-size':[0, 0, 0, 0, 0],
                   'demand-growth-rate':[0.0, 0.0, 0.0, 0.0, 0.0],
                   'potential-market-share':[0.0, 0.0, 0.0, 0.0, 0.0],
                   'product-satisfaction':[0, 0, 0, 0, 0],
                   'segment-satisfaction':[0, 0, 0, 0, 0],
                   'units-sold':[0, 0, 0, 0, 0],
                   'leftover-inventory': [0, 0, 0, 0, 0],
                   'production-buffer': [None, None, None, None, None],
                   'm-basic-growth': [0.0, 0.0, 0.0, 0.0, 0.0],
                   'p-basic-growth': [0.0, 0.0, 0.0, 0.0, 0.0],
                   'm-potential-model': [0.0, 0.0, 0.0, 0.0, 0.0],
                   'p-potential-model': [0.0, 0.0, 0.0, 0.0, 0.0],
                   'm-satisfaction-model': [0.0, 0.0, 0.0, 0.0, 0.0],
                   'p-satisfaction-model': [0.0, 0.0, 0.0, 0.0, 0.0],
                   'marketing-forecast': [0.0, 0.0, 0.0, 0.0, 0.0],
                   'production-forecast': [0.0, 0.0, 0.0, 0.0, 0.0]
                   })

# defining q as False to engage while loop
q = False

# function definitions
def quitter(var):
    global q
    if str(var).lower() == 'quit':
        q = True

def find_market_size(num):
    try:
        target_product = products[num-5]
        market_size_element = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div/div[{num}]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/table/tbody/tr[1]/td[2]')
        market_size = int(market_size_element.text.replace(',', '').replace(' ', ''))
        return market_size
    except Exception as e:
        print(f'Error processing market size for {target_product}: {e}')

def find_demand_growth_rate(num):
    try:
        target_product = products[num-5]
        demand_growth_rate_element = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div/div[{num}]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/table/tbody/tr[4]/td[2]')
        demand_growth_rate = float(demand_growth_rate_element.text.replace('%', '').replace('.', '').replace(' ', ''))*0.001
        return demand_growth_rate
    except Exception as e:
        print(f'Error processing demand growth rate for for {target_product}: {e}')

def find_potential_market_share(num):
    try:
        tr_xpath = '/html/body/div/div/div/div/div[10]/div/div[3]/div[2]/div/table/tbody/tr'
        rows = driver.find_elements(By.XPATH, tr_xpath)
        target_product = products[num]
        for row in rows:
            product_td = row.find_element(By.XPATH, 'td[1]')
            product = product_td.text
            if product.lower() == target_product:
                value_td = row.find_element(By.XPATH, f'td[{num+2}]')
                value = value_td.text
                potential_market_share = float(value.strip().replace('%', ''))/100
                return potential_market_share
    except Exception as e:
        print(f'Error processing potential market share for {target_product}: {e}')

def find_product_satisfaction(num):
    try:
        tr_xpath = f'/html/body/div[1]/div/div/div/div[{num}]/div/div[1]/div[2]/div[3]/table/tbody/tr'
        rows = driver.find_elements(By.XPATH, tr_xpath)
        target_product = products[num-5]
        for row in rows:
            product_td = row.find_element(By.XPATH, 'td[1]')
            product = product_td.text
            if product.lower() == target_product:
                value_td = row.find_element(By.XPATH, 'td[15]')
                product_satisfaction = value_td.text.replace(' ', '')
                return int(product_satisfaction)
    except Exception as e:
        print(f'Error processing product satisfaction for {target_product}: {e}')
        
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
                print(f"Error accessing td[15] (product satisfaction) in div[{num}]: {e}")
        return sum_td_15
    except Exception as e:
        print(f'Error processing segment satisfaction div[{num}]: {e}')

def find_units_sold(num):
    try:
        tbody_xpath = '/html/body/div[1]/div/div/div/div[4]/div/div[1]/div[3]/div/table/tbody'
        rows = driver.find_elements(By.XPATH, f'{tbody_xpath}/tr')
        target_product = products[num]
        for row in rows:
            product_td = row.find_element(By.XPATH, 'td[1]')
            product = product_td.text.replace(',', '').replace(' ', '')
            if product.lower() == target_product:
                value_td = row.find_element(By.XPATH, 'td[3]')
                units_sold = value_td.text.replace(',', '').replace(' ', '')
                return int(units_sold)
    except Exception as e:
        print(f'Error processing units sold for {target_product}: {e}')
        
def find_leftover_inventory(num):
    try:
        tbody_xpath = '/html/body/div[1]/div/div/div/div[4]/div/div[1]/div[3]/div/table/tbody'
        rows = driver.find_elements(By.XPATH, f'{tbody_xpath}/tr')
        target_product = products[num]
        for row in rows:
            product_td = row.find_element(By.XPATH, 'td[1]')
            product = product_td.text.replace(',', '').replace(' ', '')
            if product.lower() == target_product:
                value_td = row.find_element(By.XPATH, 'td[4]')
                units_sold = value_td.text.replace(',', '').replace(' ', '')
                return int(units_sold)
    except Exception as e:
        print(f'Error processing units sold for {target_product}: {e}')


# find directory path
py_file_path = __file__
file_path = py_file_path.replace(f'{Path(__file__).name}', '')

# Attempt to retrieve chrome driver path
## If unable, write new file `chrome-driver-path.txt`
driver_attempt = os.path.join(file_path, 'chrome-driver-path.txt')
if not os.path.exists(driver_attempt) or os.path.getsize(driver_attempt) == 0:
    with open(driver_attempt, 'w') as file:
        chrome_driver_path = input('Enter Chrome driver path---------------------------------->')
        file.write(chrome_driver_path)
else:
    with open(driver_attempt, 'r') as file:
        chrome_driver_path = file.read()

# Attempt to retrieve browser path
## If unable, write new file `browser-path.txt`
browser_attempt = os.path.join(file_path, 'browser-path.txt')
if not os.path.exists(browser_attempt) or os.path.getsize(browser_attempt) == 0:
    with open(browser_attempt, 'w') as file:
        browser_path = input('Enter browser path---------------------------------------->')
        file.write(browser_path)
else:
    with open(browser_attempt, 'r') as file:
        browser_path = file.read()

while not q:

# inputs
    username = str(input('Enter username-------------------------------------------->'))
    quitter(username)
    if q:
        break

    password = str(input('Enter password-------------------------------------------->'))
    quitter(password)
    if q:
        break
    
    while True:
        try:
            round_num_temp = input('Enter round number: ')
            quitter(round_num_temp)
            if q:
                break
            round_num = int(round_num_temp)
            break
            
        except ValueError:
            print('\nInvalid input. Please enter round number as an integer.\n')
    
    for market in df['market']:
        product_temp = str(input(f'Enter {market} product name: ')).lower()
        quitter(product_temp)
        if q:
            break
        products.append(product_temp)

# initialize b and q
    b = False
    q = False
    
    while True:
        try:
            y_n = str(input("Are all markets' forecast buffers the same? [y/n]----->")).lower()
            quitter(y_n)
            if q:
                break
            if y_n == 'y' or y_n == 'yes':
                while True:
                    try:
                        production_buffer = float(input('Enter production buffer---------------------------------->'))
                        quitter(production_buffer)
                        if q:
                            break
                        df[['production-buffer']] = production_buffer
                        b = True
                        break
                    except ValueError:
                        print('\nPlease enter buffer in the format #.##\n')
            elif y_n == 'n' or y_n == 'no':
                market_num = 0
                for market in df['market']:
                    while True:
                        try:
                            production_buffer_temp = float(input(f'Enter {market} production buffer: '))
                            quitter(production_buffer_temp)
                            if q:
                                break
                            df.iloc[market_num, 8] = production_buffer_temp
                            market_num += 1
                        except ValueError:
                            print('\nPlease enter buffer in the format #.##\n')
                b = True
            else:
                print('\nInvalid input. Please enter "y" or "n".')
            if b:
                break
        except ValueError as e:
            print(f'\nProduction buffer ValueError: {e}. Please add to `Issues` page.')
                                     
    wait_time = int(input('Enter step wait time (sec; >1)----->'))
    
    print('\nProcessing...\n')
    time.sleep(wait_time)

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
        button = driver.find_element(By.XPATH, step)
        button.click()
        time.sleep(wait_time)
    
    tbody_xpath = '/html/body/div[3]/div/div/div/div/div[1]/table/tbody'
    rows = driver.find_elements(By.XPATH, f'{tbody_xpath}/tr')
    for row_index, row in enumerate(rows, start=1):
        row_text = ""
        for attempt in range(3):
            try:
                row_text = row.text
                if row_text:
                    break
            except Exception as e:
                print(f"Attempt {attempt + 1}: Failed to get text for row {row_index} - {e}")
                time.sleep(1)
        if row_text:
            row_list = row_text.split()
            try:
                if row_list and row_list[0].isdigit():
                    round_num_attempt = int(row_list[0])
                    if round_num_attempt == round_num:
                        button_xpath = f'{tbody_xpath}/tr[{row_index}]/td[2]/a'
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
                        button = driver.find_element(By.XPATH, button_xpath)
                        button.click()
                        time.sleep(wait_time + 2)
                        tabs = driver.window_handles
                        driver.switch_to.window(tabs[-1])
                        del password
                        del username
                        break
            except ValueError:
                print(f"Row {row_index} does not start with a number: {row_text}")
            except NoSuchElementException:
                print(f"Button not found for row {row_index}.")
        else:
            print(f"No text found for row {row_index} after multiple attempts.")

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
    
# inputting units sold
    for i in range(0, 5):
        df.iloc[i, 6] = find_units_sold(i)

# inputting leftover inventory
    for i in range(0, 5):
        df.iloc[i, 7] = find_leftover_inventory(i)
    
    units_sold = df['units-sold']
    demand_growth_rate = df['demand-growth-rate']
    production_buffer = df['production-buffer']
    potential_market_share = df['potential-market-share']
    leftover_inventory = df['leftover-inventory']
    market_size = df['market-size']
    product_satisfaction = df['product-satisfaction']
    segment_satisfaction = df['segment-satisfaction']
    
# calculating basic growth forecasts
    df['m-basic-growth'] = units_sold * (1 + demand_growth_rate) * 0.9
    df['p-basic-growth'] = units_sold * demand_growth_rate * production_buffer

# calculating potential market share forecasts
    df['m-potential-model'] = market_size * (1 + demand_growth_rate) * potential_market_share * 0.9
    df['p-potential-model'] = market_size * (1 + demand_growth_rate) * potential_market_share * production_buffer

# calculating satisfaction score share forecasts
    df['m-satisfaction-model'] = market_size * (1 + demand_growth_rate) * (product_satisfaction / segment_satisfaction) * 0.9
    df['p-satisfaction-model'] = market_size * (1 + demand_growth_rate) * (product_satisfaction / segment_satisfaction) * production_buffer

# calculating averaged forecasts
    df['marketing-forecast'] = (df['m-basic-growth'] + df['m-potential-model'] + df['m-satisfaction-model']) / 3
    df['production-forecast'] = (df['p-basic-growth'] + df['p-potential-model'] + df['p-satisfaction-model']) / 3 - leftover_inventory

# print market name and forecasts
    print(df[['market', 'marketing-forecast', 'production-forecast']])
    
# querying system with query counter
    query_count = 1
    while True:
        query = str(input(f"\nEnter query, one of: \n\n{(', '.join(df.columns[1:])).replace('-', ' ')}, or quit to quit.\n\nQuery[{query_count}]: ")).lower().replace(' ', '-')
        quitter(query)
        if q:
            break
        while query:
            if query not in df.columns or query == 'market':
                print('\nQuery request invalid.')
                query = False
            else:
                query_count += 1
                print('\n', df[['market', f'{query}']])
                query = False

