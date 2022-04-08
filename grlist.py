from bs4 import BeautifulSoup
import requests
from csv import writer

import pandas as pd
from pandas_profiling import ProfileReport

url=input("Enter a goodreads list url \n >>")
page=requests.get(url)

soup= BeautifulSoup(page.content, 'html.parser')
lists=soup.find_all('tr')

with open('goodreadsList.csv', 'w', encoding='utf8', newline='') as f:
    thewriter=writer(f)
    heading=["Rank", "Name", "Author", "Rating"]
    thewriter.writerow(heading)

    for list in lists:
        ranking=list.find('td', class_="number").text
        title=list.find('a', class_="bookTitle").span.text
        author=list.find('a', class_="authorName").span.text
        ratingString=(list.find('span', class_="minirating").text[1:5])
        try:
            rating=float(ratingString)
        except:
            rating=4
        data=[ranking, title, author,rating]
        print(data)
        thewriter.writerow(data)

df=pd.read_csv("goodreadsList.csv")

profile=ProfileReport(df)
profile.to_file(output_file="GoodreadsListReport.html")