import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


df_brand_with_model = pd.read_pickle('car_dataset.pkl')

def insert_model_prices(brand, model):
    for year in range(2016,2023):
        response_from_wm = requests.get(f"http://archive.org/wayback/available?url=http://www.arabalar.com.tr/{brand}/{model}/{year}&timestamp={year}")
        
        try:
            response_from_wm = response_from_wm.json()
        except ValueError:
            print("JSON DECODE ERROR BUT CONTINUING...")
            continue 

        print(response_from_wm)
        
        if response_from_wm['archived_snapshots'] == {}:
            continue
        

        wm_url = response_from_wm['archived_snapshots']['closest']['url']
        # headers = {'User-Agent': 'Mozilla/5.0'}
        # print("URL: " + wm_url + "\nCONTENT: \n")
        
        response = requests.get(wm_url)
        soup = BeautifulSoup(response.content, 'lxml')

        prices_html = soup.find_all('li', {'class': 'list-group-item'})
        prices_element = list(prices_html[0])
        prices_element = str(prices_element)

        # print(prices_element)
        start_index = prices_element.index('span') + 5
        # print(prices_element[start_index:])
        stop_index  = prices_element.rindex('<a') - 4
        # print(prices_element[:stop_index])
        try:
            price = int(prices_element[start_index:stop_index].replace('.', ''))
        except:
            price = np.nan    
        # print("price: " + str(price) + " TYPE: " + str(type(price)))

        df_brand_with_model.loc[(df_brand_with_model['brand'] == brand) & (df_brand_with_model['model'] == model), str(year)] = price

for brand in df_brand_with_model['brand'].unique():
    for model in df_brand_with_model[df_brand_with_model['brand'] == brand]['model']: 
        insert_model_prices(brand, model)

