from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import time

def scrape_coinnames():

    page = requests.get('https://coinmarketcap.com/')
    soup = BeautifulSoup(page.content, 'html.parser')

    coin_types = []
    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coindata = json.loads(data.contents[0])['props']['initialState']['cryptocurrency']['listingLatest']['data']

    for coin_name in coindata:
        coin_types.append(coin_name['slug'])

    return coin_types

def scrape_indiv_prices(coin_types, slug):

    res = {}

    if slug in coin_types:
        url = 'https://coinmarketcap.com/currencies/'+ slug
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        data = soup.find_all('div', {'class':'priceValue___11gHJ'})
        price = data[0].text
        res['coin'] = slug
        res['price'] = price

        return res

    else:
        return None

def init_prices(coin_types):

    res = {}

    slug_types = coin_types[0:5]
    for slug in slug_types:
        url = 'https://coinmarketcap.com/currencies/'+ slug
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        data = soup.find_all('div', {'class':'priceValue___11gHJ'})
        price = data[0].text
        res[slug] = {}
        res[slug]['coin'] = slug
        res[slug]['price'] = price
    
    return res


def main():
    coin_types = scrape_coinnames()
    res = init_prices(coin_types)
    return res, coin_types

def main_indiv(slug):
    coin_types = scrape_coinnames()
    res = scrape_indiv_prices(coin_types, slug)
    return res