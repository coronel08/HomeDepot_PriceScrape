# https://www.programiz.com/python-programming/dictionary
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import random
from webdriver_manager.chrome import ChromeDriverManager
import re


def main():
    filename = 'Appliance-Pricing-10-1-18.xlsx'
    bot = HomeDepotBot(filename)
    bot.webscrapeHomeDepot()


class HomeDepotBot():
    """ 
    A class that takes the excel file in /data_files provided in the main() function and scrapes the Home Depot Website for pricing on the appliance by model #
    """

    def __init__(self, file):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.path = os.path.join(os.getcwd(), 'data_files')
        self.dataFile = os.path.join(self.path, file)
        df = pd.read_excel(self.dataFile, engine='openpyxl')
        self.df = df[df['CATEGORY'] == 'Fabric Care']

    def getModel(self):
        dfModel = self.df['MATERIAL']
        dfPrice = self.df['PRICE 10/1/2018']
        return dfModel

    """ Method writes pandas dataframe to new excel file called test.xlsx"""

    def writeToExcelFile(self, hdPrice):
        self.df["hdprice"] = hdPrice.values()
        print('---------------Write to Excel --------------')
        self.df.to_excel('Script_export.xlsx', sheet_name='sheet1')

    """ 
    Method to run the webscraper bot. It iterates through a list of model #'s and returns a dataframe with competitors pricing. 
    Writes to a new excel file in main directory
    """

    def webscrapeHomeDepot(self):
        dfModel = self.getModel()
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
                    _, price, *trash = priceWrapper.split('$')
                    price = re.search(r'\d+', price).group()
                    hdPrice[model] = int(price)//100
                else:
                    hdPrice[model] = 'NA'
            except (NoSuchElementException, StaleElementReferenceException):
                hdPrice[model] = 'NA'
            print(model, hdPrice[model])
        writeToExcelFile = self.writeToExcelFile(hdPrice)


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
