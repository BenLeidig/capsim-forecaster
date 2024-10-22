#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 14:21:38 2024

@author: benleidig
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

username=str(input('Enter username: '))
password=str(input('Enter password: '))
wait_time=int(input('Enter wait time (sec; at least 3 is recommended): '))
chrome_driver_path = '/Users/benleidig/Downloads/chromedriver-mac-arm64/chromedriver'
browser_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"

options = Options()
options.binary_location = browser_path
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://ww2.capsim.com/login/')

username_field = driver.find_element(By.ID, 'username')
username_field.send_keys(username)
password_field = driver.find_element(By.ID, 'password')
password_field.send_keys(password)
sign_in_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/main/div[1]/form/div[3]/button')
sign_in_button.click()

time.sleep(wait_time)

enter_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div/div[5]/a')
enter_button.click()

time.sleep(wait_time)

reports_button = driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/ul/li[4]/a')
reports_button.click()

time.sleep(wait_time)

simulation_reports_button = driver.find_element(By.XPATH, '/html/body/nav/div/div[2]/ul/li[4]/ul/li[2]/a')
simulation_reports_button.click()

time.sleep(wait_time)

round_num_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div/div[1]/table/tbody/tr/td[2]/a')
round_num_button.click()

time.sleep(wait_time)

tabs = driver.window_handles
driver.switch_to.window(tabs[-1])

time.sleep(wait_time)

traditional_market_size = driver.find_element('/html/body/div/div/div/div/div[5]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div/table/tbody/tr[1]/td[2]/span')
traditional_market_size = ','.split(traditional_market_size.text)
print(traditional_market_size)

