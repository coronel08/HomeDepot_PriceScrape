import time
import random
import os
import requests
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import csv
# from dotenv import load_dotenv


def main():
    file = "Appliance-Pricing-10-1-18.xlsx"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    seleniumWebScrape(file, driver)


def seleniumWebScrape(file, driver):
    """ Webscrapes HomeDepot website and writes to a new file """
    hdPrice = {}
    df = readFile(file)
    dfModel = getModel(df)
    # List below used for testing scraping
    # testList = ['WGD4985EW', 'MVW7232HW', 'WED4616FW']

    for model in dfModel:
        scrapeModelPrice(driver, model, hdPrice)
    writeFile(df, hdPrice)


def readFile(file):
    """ Reads excel file and returns a df """
    path = os.path.join(os.getcwd(), 'data_files')
    dataFile = os.path.join(path, file)
    df = pd.read_excel(dataFile, engine='openpyxl')
    return df


def getModel(df):
    """ Returns the model number for the appliances SeleniumWebscraper function """
    df = df[df['CATEGORY'] == 'Fabric Care']
    dfModel = df['MATERIAL']
    return dfModel


def scrapeModelPrice(driver, model, hdPrice):
    """ 
    Searches appliance models for price, if no price available returns NA  
    Also prints out model and price 
    """
    resposne = driver.get('https://www.homedepot.com/s/' + model)
    time.sleep(random.randint(1, 3))
    try:
        priceWrapper = driver.find_element_by_class_name(
            'price-detailed__wrapper').text
        if (priceWrapper.__contains__('$')):
            _, price, *trash = priceWrapper.split('$')
            hdPrice[model] = int(price)//100
        else:
            hdPrice[model] = 'NA'
    except (NoSuchElementException, StaleElementReferenceException):
        hdPrice[model] = 'NA'
    print(model, hdPrice[model])


def writeFile(df, hdPrice):
    print('Writing to Excel File ...')
    df["hdprice"] = hdPrice.values()
    df.to_excel('export.xlsx', sheet_name='sheet1')


if __name__ == "__main__":
    main()
