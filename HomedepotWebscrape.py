# https://www.programiz.com/python-programming/dictionary
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import random


def main():
    filename = '/Appliance-Pricing-10-1-18.xlsx'
    bot = HomeDepotBot(filename)
    bot.webscrapeHomeDepot()


class ExcelFile:
    def __init__(self, file):
        self.dataFile = os.getcwd() + file
        df = pd.read_excel(self.dataFile, engine='openpyxl')
        self.df = df[df['CATEGORY'] == 'Fabric Care']
        # self.writer = pd.ExcelWriter(self.dataFile, engine='openpyxl')

    """ Uses Pandas to read excel file and return a series of the Model """

    def getModel(self):
        dfModel = self.df['MATERIAL']
        dfPrice = self.df['PRICE 10/1/2018']
        return dfModel

    """ Figure out how to write to Column in another class"""

    def writeToExcelFile(self, dfCount, hdPrice):
        pass
        # self.df.loc[dfCount, ["hdprice"]] = hdPrice.values()


class HomeDepotBot():
    def __init__(self, file):
        self.driver = webdriver.Chrome()
        self.file = file
        self.excelFile = ExcelFile(file)

    def webscrapeHomeDepot(self):
        dfModel = self.excelFile.getModel()
        # Figure out how to write to file later
        writeToExcelFile = self.excelFile.writeToExcelFile()
        dfCount = 0
        hdPrice = {}
        # For testing homedepot Scrape, replace dfModel with testList in the loop below
        # testList = ['WGD4985EW', 'MVW7232HW', 'WED4616FW']

        for model in dfModel:
            response = self.driver.get('https://www.homedepot.com/s/' + model)
            time.sleep(random.randint(1, 3))
            try:
                priceWrapper = self.driver.find_element_by_class_name(
                    'price-detailed__wrapper').text
                if (priceWrapper.__contains__('$')):
                    splitPrice = priceWrapper.split('$')
                    hdPrice[model] = int(splitPrice[1])//100
                else:
                    price = 'NA'
                    hdPrice[model] = price
            except (NoSuchElementException, StaleElementReferenceException):
                hdPrice[model] = 'NA'
            print(hdPrice[model])
            dfCount += 1


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
