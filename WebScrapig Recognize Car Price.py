import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import urllib3
import mysql.connector
connect_to_dbPrice=mysql.connector.connect(user='root', password='',
                                           host='127.0.0.1', database='car_price')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
css_selector_list=['span.bama-ad-detail-title__subtitle:nth-child(1)','span.bama-ad-detail-title__subtitle:nth-child(3)','.bama-ad-detail-price__price-text','p.dir-ltr','div.bama-vehicle-detail-with-icon__detail-holder:nth-child(4) > p:nth-child(3)','div.bama-vehicle-detail-with-icon__detail-holder:nth-child(5) > p:nth-child(3)','div.bama-vehicle-detail-with-icon__detail-holder:nth-child(3) > p:nth-child(3)']
car_dict={1:'/car/renault-tondar90', 2:'/car/peugeot-206sd', 3:'/car/peugeot-pars', 4:'/car/peugeot-207', 5:'/car/dena', 6:'/car/saina', 7:'/car/quick', 8:'/car/tara', 9:'/car/shahin', 10:'/car/peugeot-206ir', 11:'/car/peugeot-405', 12:'/car/pride'}
link_list=[]
home_page='https://bama.ir'
headers = {'User-Agent': 'c5af3997-059e-4cb2-a70b-24960314efe5'}
print('1-L90\n2-206SD\n3-Pars\n4-207\n5-Dena\n6-Saina\n7-Quick\n8-Tara\n9-Shahin\n10-206\n11-405\n12-Pride\n')
car_code=int(input('Enter number of the desired car based on the list above: '))
model_car_link=home_page+(car_dict.get(car_code))
browser=webdriver.Firefox()
source=browser.get(model_car_link)
time.sleep(1)
home_elemement=browser.find_element(By.TAG_NAME ,'body')
no_of_pagedown=50
while no_of_pagedown>0:
    home_elemement.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedown-=1
cars_elements=browser.find_elements(By.CLASS_NAME,'bama-ad-holder')
timeout=5
for post in cars_elements:
    HTML_post=post.get_attribute('outerHTML')
    if (re.search(r'توافقی',post.text))==None:
        post_soup=BeautifulSoup(HTML_post,'html.parser')
        find_link=post_soup.find('a')
        link=find_link.get('href')
        link_list.append(link)
for link in link_list:
    feature_car_link=home_page+link
    session = requests.Session()
    link_text = session.get(feature_car_link, headers=headers, verify=False)
    link_soup=BeautifulSoup(link_text.text,'html.parser')
    cars_features=[]  
    for selected_tag in css_selector_list:
        feature_tag=link_soup.select(selected_tag)
        text_tag=re.sub(r'\s+','',(feature_tag[0]).text)
        if (re.search(r'صفر',text_tag))!=None:
            text_tag=0
        cars_features.append(text_tag)
    print(cars_features)
    for feature in cars_features:
        cursor=connect_to_dbPrice.cursor()
        cursor.execute('INSERT INTO Car_Choose VALUES(%i,\'%s\',%i,\'%s\',\'%s\',\'%s\',\'%s\')' %(cars_features[0],cars_features[1],cars_features[2],cars_features[3],cars_features[4],cars_features[5],cars_features[6]))
        connect_to_dbPrice.commit()
        connect_to_dbPrice.close()
            