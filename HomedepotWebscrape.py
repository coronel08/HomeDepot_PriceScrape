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


def main():
    bot = HomeDepotBot()
    bot.webscrapeHomeDepot()


if __name__ == "__main__":
    main()


# Using bs4 to webscrape (Not Working)
# def bs4Webscrape():
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
#     hdprice = {}
#     dataFile = os.getcwd() + '/Appliance-Pricing-10-1-18.xlsx'

#     Read Excel File
#     df = pd.read_excel(dataFile, engine='openpyxl')
#     df = df[df['CATEGORY'] == 'Fabric Care']
#     dfModel = df['MATERIAL']
#     dfPrice = df['PRICE 10/1/2018']
#     dfCount = 0
#     testList = ['WGD4985EW', 'MVW7232HW', 'WED4616FW']
#     for i in testList:
#         response = requests.get(
#             url='https://www.homedepot.com/s/'+i, headers=headers)
#         page = BeautifulSoup(response.content, 'lxml')
#         try:
#             price = page.find('div', {'class': 'price-detailed__wrapper'}).text
#             print(price)
#             model = i
#             hdprice[i] = int(price)
#         except AttributeError:
#             hdprice[i] = "NA"
#         print(hdprice)
#         df.loc[dfCount, ["hdprice"]] = hdprice.values()
#         dfCount += 1

#         writer = pd.ExcelWriter(path)
#         df.to_excel(writer)
#         writer.save()
