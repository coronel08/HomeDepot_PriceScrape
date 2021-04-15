import time
import random
import os
import requests
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# Without Object Oriented programming
def main():
    file = "Appliance-Pricing-10-1-18.xlsx"
    seleniumWebScrape(file)


def seleniumWebScrape(file):
    driver = webdriver.Chrome()
    # Read Excel File
    dataFile = os.path.join(os.getcwd(), 'data_files', file)
    df = pd.read_excel(dataFile, engine='openpyxl')
    df = df[df['CATEGORY'] == 'Fabric Care']

    hdPrice = {}
    dfCount = 0
    dfModel = df['MATERIAL']
    # List below used for testing scraping
    testList = ['WGD4985EW', 'MVW7232HW', 'WED4616FW']
    for model in dfModel:
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
        print(model, hdPrice[model])
        # Need to figure out how to write to last column in excel file
        # test = df.insert(1, "hdPrice", hdPrice[model])
        # print(test)
        dfCount += 1

        # writer = pd.ExcelWriter(dataFile)
        # df.to_excel(writer)
        # writer.save


if __name__ == '__main__':
    main()
