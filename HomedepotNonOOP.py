import time
import random
import os
import requests
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# Without Object Oriented programming
def main():
    seleniumWebScrape()


def seleniumWebScrape():
    driver = webdriver.Chrome()
    hdPrice = {}
    dfCount = 0
    testList = ['WGD4985EW', 'MVW7232HW', 'WED4616FW']
    for model in testList:
        resposne = driver.get('https://www.homedepot.com/s/' + model)
        time.sleep(random.randint(1, 3))
        try:
            priceWrapper = driver.find_element_by_class_name(
                'price-detailed__wrapper').text
            if (priceWrapper.__contains__('$')):
                splitPrice = priceWrapper.split('$')
                hdPrice[model] = int(splitPrice[1])//100
            else:
                hdPrice[model] = 'NA'
        except (NoSuchElementException, StaleElementReferenceException):
            hdPrice[model] = 'NA'
        print(hdPrice)
        dfCount += 1


def readExcelFile(file):
    filename = file
    data = os.getcwd() + filename
    df = pd.read_excel(data, engine='openpyxl')
    df = df[df['CATEGORY'] == 'Fabric Care']
    dfModel = df['MATERIAL']
    dfPrice = df['PRICE 10/1/2018']
    print('Running readExcelFile function')
    return dfModel

def writeExcel():
    # writer = pd.ExcelWriter('testFile.xlsx',engine='xlsxwriter')
    # import data to write    
    # writer.save()
    pass


if __name__ == '__main__':
    main()
