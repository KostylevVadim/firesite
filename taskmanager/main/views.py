from multiprocessing import context
from django.shortcuts import render
import folium
import ssl  
import sys
import requests 
from bs4 import BeautifulSoup as BS
import math
from pymongo import MongoClient
import folium
import re


# Create your views here.

def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def map(request):
    m = folium.Map([132.262, 44.0062], zoom_start=5)
    folium.Marker([132.262, 44.0062],folium.Icon(color='red')).add_to(m)
    m = m._repr_html_()
    context = {
        'm': m,
    }
    return render(request, 'main/map.html', context)

def news(request):
    r = requests.get("https://russian.rt.com/tag/lesnie-pojari")
    html = BS(r.content, 'html.parser')
    el1 = html.select('.card_all-new')
    str1 = []
    i=0
    for el in el1:
#    print(el.text)
        str1.append(el.text)
        i=i+1
    
    titles = []
    news = []
    date = []

    for ba in range(i):
        str2 = str1[ba].splitlines()
        for a in range(len(str2)):
            if a%3 == 1:
                titles.append(str2[a])
            if a%3 == 0:
                news.append(str2[a])
            if a%3 == 2:
                date.append(str2[a])
    while '            ' in titles:
        titles.remove('            ')
    while '' or '\t' in news:
        news.remove('')
        news.remove('\t')
    while '            ' in date:
        date.remove('            ')
    for x in range(len(date)):
        date[x] = re.sub("\s+", " ", date[x])

    Lastnews = {
        'title': titles,
        'news': news,
        'date': date
    }
    data = []

    for i in range(len(titles)):
        New = {
            'title' : titles[i],
            'news': news[i],
            'date': date[i]
        }
        data.append(New)
    
    context = {
        'data' : data
    }
    return render(request, 'main/lastnews.html',context)

def search(request):
    client = MongoClient('localhost', 27017)
    db = client.Databaseoffire
    col = db.Collectionoffire
    s = '13.04.2014'
    x = 1
    s = request.GET.get('q')
    x = request.GET.get('q1')
    if s and x:
        query = {"date": s}
        map = folium.Map()
        for date in col.find(query, {"_id":0}):
            lat = float(date["lat"])
            lon = float(date["lon"])
            type_id = int(date["type_id"])
            print(lat, lon, math.isnan(lat)!=1, math.isnan(lon)!=1, x, type_id, int(x)==type_id)
            if  math.isnan(lat) != 1 and math.isnan(lon) != 1 and int(x)==type_id:
                x = int(x)
                if x == 1 :
                    folium.Marker(location=[lat,lon], popup = str(lat) + str(lon)+" Неконтролируемый пал").add_to(map)
                if x == 2 :
                    folium.Marker(location=[lat,lon], popup = str(lat) + str(lon)+" Торфяной пожар").add_to(map)
                if x == 3 :
                    folium.Marker(location=[lat,lon], popup = str(lat) + str(lon)+" Лесной пожар").add_to(map)
                if x == 4 :
                    folium.Marker(location=[lat,lon], popup = str(lat) + str(lon)+" Природный пожар").add_to(map)
                if x == 5 :
                    folium.Marker(location=[lat,lon], popup = str(lat) + str(lon)+" Контролируемый пал").add_to(map)
        map = map._repr_html_()
        context = {
            'map': map
        }
        print("I am here")
        return render(request, 'main/search.html', context)
    else:
        
        map = folium.Map()
        map = map._repr_html_()
        context = {
            'map': map,
        }
        return render(request, 'main/search.html', context)


def important(request):
    file = open('main\RulesforNature.pdf','r')
    context = {
        'file': file
    }
    return render(request, 'main/important.html', context)