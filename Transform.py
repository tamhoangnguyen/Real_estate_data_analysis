import pandas as pd
import numpy as np

def convert_price(price):
    convert = price.split(' ')
    price = float(convert[0])
    if convert[1] == 'tỷ':
        return price * 1000000000
    elif convert[1] == 'triệu':
        return price * 1000000  
    else:
        return price * 1000

def transform_data(df):
    column = ['Price','Area', 'Price_Per_Area', 'Bedroom', 'Bathroom', 'Location', 'Title']
    df_2 = pd.DataFrame(df,columns=column) #Tạo df mới
    df_2 = df_2[df_2['Price'] != 'Giá thỏa thuận'] #Loại bỏ giá trị không phù hợp khỏi cột Price
    df_2['New_Price'] = df_2['Price'].apply(convert_price)
    df_2['New_Area'] = df_2['Area'].apply(lambda x: float(x.split(' ')[0]))
    df_2['New_Price_Per_Area'] = df_2['Price_Per_Area'].apply(lambda x : float(x.split(' ')[0]) * 1000000)
    df_2['District'] = df_2['Location'].apply(lambda x: x.split(',')[0])
    df_2['City'] = df_2['Location'].apply(lambda x: x.split(',')[1])
    column_2 = ['Title','New_Area','New_Price_Per_Area','Bedroom','Bathroom','District','City','New_Price']
    df_3 = df_2[column_2]
    df_3 = df_3.drop_duplicates(subset = 'Title')
    return df_3


