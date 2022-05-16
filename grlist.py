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
wantReport=(input("Do you want an analysis report? (Y/N) \n >>")).upper()

dataName=input("Save Database As: \n >>")
dataNameOutput=dataName+".csv"

if wantReport == "Y":
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
    heading=["Rank", "Name", "Author", "Average Rating", "Number Of Ratings"]
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
            numberOfRatingsString=list.find('span', class_="minirating").text.strip()[12:].replace(",","")
            numberOfRatings=""
            for character in numberOfRatingsString:
                if character.isdigit():
                    numberOfRatings=numberOfRatings+str(character)
            data=[ranking, title, author,rating, numberOfRatings]
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

print((" \n The data has been succesfully exported as "+dataNameOutput+"\n").upper())

if wantReport == "Y" :
    df=pd.read_csv(dataNameOutput)
    profile=ProfileReport(df)
    profile.to_file(output_file=outputNameHtml)

wantFiltered=input("Do you want a filtered recommendation with high ratings from 15000+ reviewers? (y/n)\n").upper()

if wantFiltered=="Y":
    df=pd.read_csv(dataNameOutput)
    fourPlus=(df["Average Rating"]>=4)
    rated=df[fourPlus]
    print(rated)
    fifteen=(df["Number Of Ratings"]>15000)
    verified=df[fifteen]
    print(verified)
    optimized=verified[fourPlus]
    print(optimized)
    optimized.to_csv(dataName+"Filtered.csv")

    print((" \n The filtered data has been succesfully exported as "+dataName+"Filtered.csv\n").upper())