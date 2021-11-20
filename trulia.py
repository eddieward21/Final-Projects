from bs4 import BeautifulSoup
import requests
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib as plt
from csv import writer
import re
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def house_search(town, state):
    url = "https://www.trulia.com/{state}/{town}/".format(state=state, town=town)
    response = requests.get(url, headers = {"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    houses = soup.find_all('div', attrs = {'data-hero-element-id': 'srp-home-card'})

    with open(town+".csv", 'w', newline = '', encoding= 'utf8') as f:
        my_writer = writer(f)
        header = ['Price', "# of Beds"]
        my_writer.writerow(header)
        for house in houses:
            price = house.find('div', attrs = {'data-testid': 'property-price'}).text.strip()
            beds = house.find('div', attrs = {'data-testid':'property-beds'}).text.strip()
            row = [price, beds]
            my_writer.writerow(row)
            
    
    houses_df = pd.read_csv(town+'.csv')
    x = houses_df['# of Beds']
    x = x.str[0]
    x = pd.to_numeric(x)
    
    y = houses_df['Price']
    y = y.str.replace(',', '').str.replace('$', '')
    y = pd.to_numeric(y)
    
    #print(x.ndim, x.shape)
    #print(y.ndim, y.shape)
    x = x.values.reshape(-1,1)
    y = y.values.reshape(-1,1)

    model = LinearRegression()
    model.fit(x,y)
    
    mean_beds = x.mean()
    mean_price = y.mean()
    print(mean_beds, mean_price)
    sns.set_style('darkgrid')
    sns.displot(houses_df['# of Beds'])
    
    sns.jointplot(data = houses_df, x = '# of Beds', y = 'Price')
    
house_search("New Orleans", "LA")




