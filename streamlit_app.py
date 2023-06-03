import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


st.title('Auto Brands in Turkey - Failed')

st.write('This is a failed attempt to create a dataset of auto brands in Turkey.')

st.write('The dataset is created by scraping the website [arabalar.com.tr](http://www.arabalar.com.tr/).')


st.image('audi.png')
st.image('audi-a3.png')
st.markdown('### Indexing of the website: ')
st.markdown('- ##### arabalar.com.tr/brand/model/')
st.markdown('- ##### arabalar.com.tr/audi/')
st.markdown('- ##### arabalar.com.tr/audi/a3/')

body = """
df = pd.DataFrame(columns=['brand', 'model', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', 'checked'])
brands = ["audi", "bmw", "citroen", "dacia", "fiat", "ford", "honda", "hyundai", "jeep", "kia", "mercedes", "mitsubishi", "nissan", "opel", "peugeot", "renault", "skoda", "suzuki", "toyota", "volkswagen", "volvo"]

def models(brand):
    url = f"http://www.arabalar.com.tr/{brand}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    time.sleep(1)
    models_soup = soup.find_all('a', {'class': 'list-group-item'})
    models_soup = list(models_soup)
    
    models_list = []    
    for model in models_soup:
        models_list.append(model.text.lower().replace(' ', '-'))

    return models_list


for brand in brands:
    for model in models(brand):
        df = df.append({'brand': brand, 'model':model}, ignore_index=True)

df.to_pickle('car_dataset.pkl')        
"""
st.markdown("#")
st.subheader('Creating the dataset with brand, model and 2016-2023 columns: ')
st.code(body, language='python', line_numbers=False)
st.markdown("##### The dataset:")
st.dataframe(pd.read_pickle('car_dataset.pkl'))


body_price = r"""
def insert_model_prices(brand, model):
    
    counter = 0

    for year in range(2016,2023):      
        
        response_from_wm = requests.get(f"http://archive.org/wayback/available?url=http://www.arabalar.com.tr/{brand}/{model}/{year}&timestamp={year}")
        print(response_from_wm)
        counter += 1

        time.sleep(np.random.randint(2, 5))

        try:
            response_from_wm = response_from_wm.json()
        except ValueError:
            print("JSON DECODE ERROR BUT CONTINUING...")
            continue 
        
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

        
        

        if counter % 15 == 0:
            df_brand_with_model.loc[df_brand_with_model['checked'] == 1].to_pickle('car_dataset.pkl')

            #delete first 10 rows of df_brand_with_model
            #df_brand_with_model = df_brand_with_model.iloc[10:]

            print("SAVED TO PICKLE")
            time.sleep(5)


reading_index = df_brand_with_model['checked'].isna().idxmax()

for brand in df_brand_with_model['brand'][reading_index:].unique():
    for model in df_brand_with_model[df_brand_with_model['brand'] == brand]['model'][10:]: 
        insert_model_prices(brand, model)
        df_brand_with_model.loc[(df_brand_with_model['brand'] == brand) & (df_brand_with_model['model'] == model), 'checked'] = 1
"""

st.subheader('Inserting prices to the dataset by years: ')
st.code(body_price, language='python', line_numbers=False)
st.caption('OUTPUT:')
st.caption('<Response [200]>')
st.caption('<Response [200]>')
st.caption('<Response [200]>')
st.caption('<Response [200]>')
st.caption('<Response [200]>')
st.caption('<Response [200]>')
st.caption('<Response [200]>')
st.caption('<Response [200]>')
st.caption('. . .')


st.markdown("#")
st.markdown("##### The dataset:")
st.image('car_dataset_prices.png')


df = pd.concat([pd.DataFrame(columns=['Time(t)', 'Number of Responses(n)']), pd.DataFrame([[1, 30], [2, 30], [3, 30], [4, 50], [5, 50], [6, 30], [7, 35], [8, 60], [9, 55], [10, 40], [11, 40], [12, 35], [13, 70], [14, 80], [15, 100], [16, 100], [18, 0], [19, 0 ], [20, 0], [21, 80], [22, 150], [23, 200], [24, 300], [25, 400], [26,500]], columns=['Time(t)', 'Number of Responses(n)'])], ignore_index=True)
st.markdown("#")
st.markdown('#### Number of Responses(n) vs Time(t):')
responses_vs_time = px.line(df, x='Time(t)', y='Number of Responses(n)')


st.plotly_chart(responses_vs_time)

st.subheader('Error Messages i got while running: ')
st.error("JSONDecodeError: Expecting value: line 1 column 1 (char 0)")
st.error("ConnectionError: HTTPConnectionPool(host='web.archive.org', port=80): Max retries exceeded with url: /web/20181219053146/http://www.arabalar.com.tr:80/mercedes/glc/2018 (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7a03c9d2d4e0>: Failed to establish a new connection: [Errno 111] Connection refused'))")
st.error("MaxRetryError: HTTPConnectionPool(host='web.archive.org', port=80): Max retries exceeded with url: /web/20181219053146/http://www.arabalar.com.tr:80/mercedes/glc/2018 (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7a03c9d2d4e0>: Failed to establish a new connection: [Errno 111] Connection refused'))")