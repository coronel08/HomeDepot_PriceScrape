# HomeDepot_PriceScrape
This project was created so that I could automatically update prices for several of our appliances/products automatically. Home Depot was our biggest competitor and to stay competitive with prices we would have to regularly adjust our prices based on their sales. 


![preview-vid](https://github.com/coronel08/HomeDepot_PriceScrape/blob/master/webscrape.gif)<br>
The logging of the model + price in the terminal and the browser are just for show. It makes for a good video, would recommend running selenium browser silent. Also I made sure to randomize the time between product searches so the IP doesn't get flagged for spamming the site. 


This Python script reads an excel sheet of all the products we received as a Distributor for Whirlpool and Maytag Appliances and returns the prices from Home Depot. We use to compare our prices periodically and manually so this saved us hundreds of hours and helped us ensure we were giving the customers the best deal.

**Reminder that spreadsheet is from 2019 because that was when I created this project, so a lot of the products will probably no longer be in production. If anyone can get me the Whirlpool/ Maytag Vendor pricing list for this year this will probably be more helpful.**  Unfortunately Covid affected our supply chain heavily and the business closed down as we were unable to receive supply and already had a lot of back ordered and delayed sales.

## Table of Contents
* [Deployment](#deployment)
* [Todo](#todo)

## Deployment
* Create virtual environemnt and then activate it
```
virtualenv venv 
<!-- Linux or Mac  -->
source venv/bin/activate
<!-- Windows -->
venv/Scripts/activate
```
* Install dependencies using "pip install -r requirements.txt"
* Download chromedriver, unzip and move to /usr/local/bin (mac/linux), for windows gogole how to install chromedriver and selenium.
```
sudo unzip {chromedriver.zip} -d /usr/bin
```
* Run the program in the terminal and it will run the script, make sure your terminal/ command line is in the folder path for this project
```
python HomedepotWebscrape.py
```

## Todo
* [x] See if script still runs and works
* [] Write to a databse or improve csv writting
* [] Improve functions and styling 
