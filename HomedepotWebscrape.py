#https://www.programiz.com/python-programming/dictionary
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
# path = "C:\\Users\\Karina\\Downloads\\PREFERRED-PRICING-10.1.2018-REVISED-7.25.18.xlsx"
path = os.getcwd()

df = pd.read_excel( path + '/Appliance-Pricing-10-1-18.xlsx', engine='openpyxl' )
df = df[df['CATEGORY'] == 'Fabric Care']
Model = df['MATERIAL']
Price = df['PRICE 10/1/2018']
count = 0

for i in Model:
    hdprice = {}
    response = requests.get(url='https://www.homedepot.com/s/?search='+i,headers=headers)
    page = BeautifulSoup(response.content, 'lxml')
    try:
        price = page.find('span', {'class': 'price__dollars'}).text.strip()
        model = page.find('h2', {'class': 'product_details modelNo'}).text.strip()
        hdprice[i] = int(price)
    except AttributeError:
        hdprice[i] = "NA"
    print(hdprice)
    df.loc[count,["hdprice"]] = hdprice.values()
    count += 1
print(df)
# writer = pd.ExcelWriter(path)
# df.to_excel(writer)
# writer.save()
