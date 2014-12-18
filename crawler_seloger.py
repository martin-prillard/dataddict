
import requests
import html5lib
import unicodedata as uni
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
import math
from pandas import Series, DataFrame
import unicodedata

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii

def convertToInt(text):
    groupe=text.split()
    tot=0
    for i,c in enumerate(groupe):
        tot+=int(c)*math.pow(1000, abs(i-len(groupe)+1))
    return int(tot)

def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        return BeautifulSoup(result.text,"html5lib")
    else:
        print 'Request failed', url
        return None
    
def getPriceByCity(pages, min, max):
    
    dataframe=[]
    dataset_path="C:/Users/MP/Dropbox/Mes documents/JWorkspace/dataddict/dataset/villes_france_90000.csv"
    dataset=pd.read_csv(dataset_path, sep=";",encoding="utf-8")
    
    names = dataset['name']
    cities = dataset['zipcode']
    idCity = 0
      
    prices=[]
    rents=[]
    
    for city in cities:
        city_min = str(city)
        city_min = city_min[:-3]

        for page in (1, pages):
            # sell
            soup = getSoupFromUrl('http://www.seloger.com/list.htm?cp='+city_min
            +'&org=advanced_search'
            +'&idtt='+str(2)
            +'&pxmin='
            +'&pxmax='
            +'&surfacemin='+str(min)
            +'&surfacemax='+str(max)
            +'&idtypebien='+str(1)
            +'&nb_pieces='
            +'&surf_terrainmin='
            +'&surf_terrainmax='
            +'&etagemin='
            +'&etagemax='
            +'&idtypechauffage='
            +'&idtypecuisine='
            +'&refannonce='
            +'&LISTING-LISTpg='+str(page))

            if (soup != None):
                prices_part,rents_part = getPrice(soup)
                prices = prices + prices_part 
                rents = rents + rents_part
            else:
                break

        mean_prices = pd.Series(prices).mean()
        mean_rents = pd.Series(rents).mean()
        dataframe.append(str(remove_accents(names.ix[idCity])) + str(city) + str(mean_prices) + str(mean_rents))
        print str(remove_accents(names.ix[idCity])), str(city), str(mean_prices), str(mean_rents)   
        idCity = idCity + 1  
    
    return dataframe

def getPrice(soup):
    prices=[]
    rents=[]
    #find the price on the sell
    balises_info = soup.find_all("a",class_="amount")
    for balise_info in balises_info:
        price = balise_info.text.split(' ')[0]
        prices.append(convertToInt(price))
    
    balises_info_rents=soup.find_all("a",class_="monthly")
    for balise_info_rent in balises_info_rents:
        rent = balise_info_rent.text
        rents.append(convertToInt(rent.split(' ')[1]))
    return prices,rents
    
    
pageMax = 2
dataframe = getPriceByCity(pageMax, 30,50)
    