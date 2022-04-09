from bs4 import BeautifulSoup
import requests
from csv import writer

import pandas as pd
from pandas_profiling import ProfileReport

#sample urls : https://www.goodreads.com/list/show/2997.Books_You_Would_Recommend_to_Strangers
# https://www.goodreads.com/list/show/2997.Books_You_Would_Recommend_to_Strangers?page=2
# https://www.goodreads.com/list/show/2398.The_Best_of_the_Best

url=input("Enter a goodreads list url \n >>")

for pageNumber in range(2,8):

    page=requests.get(url)

    soup= BeautifulSoup(page.content, 'html.parser')
    lists=soup.find_all('tr')
    
    for list in lists:
        ranking=list.find('td', class_="number").text
        title=list.find('a', class_="bookTitle").span.text
        author=list.find('a', class_="authorName").span.text
        ratingString=(list.find('span', class_="minirating").text[1:5])
        try:
            rating=float(ratingString)
        except:
            rating=0
        data=[ranking, title, author,rating]
        print(data)

    #going to the next page number
    if pageNumber==2:
        url=url+"?page="+str(pageNumber)
    else:
        url=url[:-1]+str(pageNumber)
        