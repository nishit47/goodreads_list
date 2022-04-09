from bs4 import BeautifulSoup
import requests
from csv import writer

import pandas as pd
from pandas_profiling import ProfileReport

#sample urls : https://www.goodreads.com/list/show/2997.Books_You_Would_Recommend_to_Strangers
# https://www.goodreads.com/list/show/2997.Books_You_Would_Recommend_to_Strangers?page=2
# https://www.goodreads.com/list/show/2398.The_Best_of_the_Best

url=input("Enter a goodreads list url \n >>")
page=requests.get(url)

soup= BeautifulSoup(page.content, 'html.parser')
lists=soup.find_all('tr')
numberOfBooks=soup.find('div',class_="stacked").text.strip()[:6].replace(",","")
#only works for 1000<10000 books currently .isstring() use garnu parxa
print(numberOfBooks)