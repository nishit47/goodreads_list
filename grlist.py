from bs4 import BeautifulSoup
import requests
from csv import writer

import pandas as pd
from pandas_profiling import ProfileReport

#sample urls : https://www.goodreads.com/list/show/2997.Books_You_Would_Recommend_to_Strangers
# https://www.goodreads.com/list/show/2398.The_Best_of_the_Best

url=input("Enter a goodreads list url: (make sure to put url of first page of the list)\n >>")
page=requests.get(url)
soup= BeautifulSoup(page.content, 'html.parser')

dataName=input("Save Database As: \n >>")
dataNameOutput=dataName+".csv"

outputName=input("Save Report As: \n >>")
outputNameHtml=outputName+".html"

numberOfBooksString=soup.find('div',class_="stacked").text.strip()[:8].replace(",","")

numberOfBooks=""
for character in numberOfBooksString:
    if character.isdigit():
        numberOfBooks=numberOfBooks+str(character)

numberOfPages=(int(numberOfBooks)//100)+1
loopNumber=numberOfPages+2

with open(dataNameOutput, 'w', encoding='utf8', newline='') as f:
    thewriter=writer(f)
    heading=["Rank", "Name", "Author", "Rating"]
    thewriter.writerow(heading)

    for pageNumber in range(2,loopNumber): #pageNumber=1+actualPageNumber because url changes after the inner loop
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
            thewriter.writerow(data)

        #going to the next page number
        if pageNumber==2:
            url=url+"?page="+str(pageNumber)
        elif pageNumber<11:
            url=url[:-1]+str(pageNumber)
        elif pageNumber>10 and pageNumber<101:
            url=url[:-2]+str(pageNumber)
        else:
            break #because goodreads only has 10000 viewable books on a list

df=pd.read_csv(dataNameOutput)

profile=ProfileReport(df)
profile.to_file(output_file=outputNameHtml)