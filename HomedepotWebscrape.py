# https://www.programiz.com/python-programming/dictionary
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import random
import re


class HomeDepotBot():
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        self.dataFile = os.getcwd() + '/Appliance-Pricing-10-1-18.xlsx'

    def webscrapeHomeDepot(self):
        self.driver = webdriver.Chrome()

        df = pd.read_excel(self.dataFile, engine='openpyxl')
        df = df[df['CATEGORY'] == 'Fabric Care']
        dfModel = df['MATERIAL']
        dfPrice = df['PRICE 10/1/2018']
        dfCount = 0
        testList = ['WGD4985EW', 'MVW7232HW', 'WED4616FW']

        # changed dfModel to testList for testing out in loop below
        for i in dfModel:
            hdPrice = {}
            response = self.driver.get('https://www.homedepot.com/s/'+i)
            time.sleep(random.randint(1, 3))
            try:
                priceWrapper = self.driver.find_element_by_class_name(
                    'price-detailed__wrapper').text
                if (priceWrapper.__contains__('$')):
                    splitPrice = priceWrapper.split('$')
                    price = int(splitPrice[1])//100
                else:
                    price = 'NA'
                model = i
                hdPrice[i] = price
            except (NoSuchElementException, StaleElementReferenceException):
                hdPrice[i] = 'NA'
            print(hdPrice)


bot = HomeDepotBot()
bot.webscrapeHomeDepot()


# Selenium Section
# bot = webdriver.Chrome()
# bot.get('https://www.homedepot.com/p/Maytag-5-3-cu-ft-Smart-Capable-White-Top-Load-Washing-Machine-with-Extra-Power-Button-ENERGY-STAR-MVW7232HW/312273355')
# price = bot.find_element_by_xpath(
#     '//*[@id="eco-rebate-price"]/div[1]/div[2]/span[2]')
# model = bot.find_element_by_xpath(
#     '//*[@id="root"]/div/div[3]/div/div/div[2]/div/div[1]/div/div/h2[2]')
# test = print(price.text, model.text)

# Old Way, couldnt get working
# for i in Model:
#     hdprice = {}
#     response = requests.get(url='https://www.homedepot.com/s/'+i,headers=headers)
#     page = BeautifulSoup(response.content, 'lxml')
#     try:
#         price = page.find('div', {'class': 'price__format'}).text.strip()
#         model = page.find('h2', {'class': 'product-info-bar__detail--24WIp'}).text.strip()
#         hdprice[i] = int(price)
#     except AttributeError:
#         hdprice[i] = "NA"
#     print(hdprice)
#     df.loc[count,["hdprice"]] = hdprice.values()
#     count += 1
# print(df)

# writer = pd.ExcelWriter(path)
# df.to_excel(writer)
# writer.save()
