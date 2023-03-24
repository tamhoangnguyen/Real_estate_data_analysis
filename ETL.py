import crawl_data as cd
import transfrom_data as td
import pandas as pd
from prefect import task, flow
from random import randint
from time import sleep

@task #extract data
def crawl_data(start_page,end_page):
    data_raw = cd.crawl_data(start_page,end_page)
    data_raw.to_csv(f'Information.csv',index=False) #Lưu bản data mới crawl
    return data_raw 

@task
def transform(df): #Transform data
    column = ['Title','New_Area','New_Price_Per_Area','Bedroom','Bathroom','District','City','New_Price']
    df = df[:,1:] #Loại bỏ cột id
    result = td.transform_data(df)
    df_2 = pd.DataFrame(result, columns=column)
    return df_2

@task #Load data
def load(df):
    df.to_csv('Information_transform.csv',index = False)
    return

@flow
def build_flow():
    start_page = 1
    end_page = 10
    for i in range(0,10): #Lấy dữ liệu của 20 page
        print('Flow {} is ready !'.format(i+1))
        print('Flow {} is starting ! '.format(i+1))
        df = crawl_data(start_page,end_page) #1 Crawl_data ( Extract_Data)
        print('Transform Data !')
        df_trans = transform(df) #2 Transform_data
        start_page = end_page
        end_page = end_page + 10
        print('Flow {} is success !'.format(i+1))
        print('--------------------------------')
        sleep(randint(0,3))
    load(df_trans) 

if __name__ =='__main__':
    build_flow()

