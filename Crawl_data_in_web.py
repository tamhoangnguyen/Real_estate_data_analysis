import numpy as np
from selenium import webdriver
from time import sleep
from random import randint
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome('chromedriver.exe')

url = 'https://batdongsan.com.vn/ban-nha-rieng/p'
url_elements = '.re__card-info .re__card-info-content'
url_title = ' .re__card-title'
url_region = ' .re__card-location .re__card-config-dot'

Regions,Titles, price, area, price_per_area, bedroom, bathroom = [],[],[],[],[],[],[]
#Lấy thông tin của từng trang dữ liệu
def crawl_information(x):
    if len(x) == 6:
        price.append(x[0])
        area.append(x[1])
        price_per_area.append(x[2])
        bedroom.append(x[3])
        bathroom.append(x[4])
        Regions.append(x[5])
    elif len(x) == 3:
        price.append(x[0])
        area.append(x[1])
        price_per_area.append(0)
        bedroom.append(0)
        bathroom.append(0)
        Regions.append(x[2])
    elif len(x) == 5:
        price.append(x[0])
        area.append(x[1])
        price_per_area.append(x[2])
        bedroom.append(x[3])
        bathroom.append(0)
        Regions.append(x[4])
    else:
        price.append(x[0])
        area.append(x[1])
        price_per_area.append(x[2])
        bedroom.append(0)
        bathroom.append(0)
        Regions.append(x[3])


#Lấy dữ liệu của từng trang
def crawl_data_one_page(url,page):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    #1. Lấy tiêu đề
    titles = driver.find_elements(By.CSS_SELECTOR,url_elements + url_title)
    my_titles = [x.text for x in titles]
    for x in my_titles:
        Titles.append(x)
    #2. Lấy dữ liệu
    infor_mation = []
    for n in range(1,page):
        if n == 11: # Không có dữ liệu thứ 11
            continue
        print('Crawl_data {} !'.format(n))
        information = driver.find_elements('xpath','/html/body/div[6]/div/div[1]/div[4]/div[{}]/a/div[2]/div[1]/div[1]'.format(n))
        my_information = [x.text.split('\n') for x in information]
        my_information = my_information[0]
        for i in range(len(my_information)):
            if my_information[i] != '·':
                infor_mation.append(my_information[i])
        crawl_information(infor_mation)
        infor_mation = []
        print('Crawl_data {} is success ! '.format(n))
        print('-----------------------------')
        sleep(randint(0,2))

#Tạo hàm để crawl dữ liệu
def crawl_data(start_page,end_page):
    element = 22 # 1trang bđs có 21 dữ liệu
    for i in range(start_page,end_page): 
        new_url = url + str(i)
        print('\tCrawl page {}'.format(i))
        crawl_data_one_page(new_url,element)
    column = ['Index','Price','Area','Price_Per_Area', 'BedRoom', 'Bathroom','Location','Title']
    index = np.arange(1,len(Titles))
    df2 = pd.DataFrame(list(zip(index,price, area, price_per_area, bedroom, bathroom,Regions,Titles)), columns=column)
    return df2



