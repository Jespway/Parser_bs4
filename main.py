import requests
from bs4 import BeautifulSoup
import csv

url_main = 'https://www.lego.com'
url_themes = 'https://www.lego.com/en-us/themes'

def get_soup(url, page=1):
    if page == 1:
        r = requests.get(url=url)
    else:
        url = f'{url}?page={page}&offset=0'
        r = requests.get(url=url)

    with open(file='index.html', mode='w', encoding="utf-8") as file:
        file.write(r.text)

    return BeautifulSoup(r.text, 'lxml')


def get_themes(soup):
    themes = soup.find('section').ul
    themes = themes.find_all('li')

    themes_list = []

    for theme in themes:
        themes_dict = {
            'name': theme.h2.span.text,
            'url':  f'{url_main}{theme.a.get("href")}'
        }
        
        themes_list.append(themes_dict)
    keys = themes_list[0].keys()

    with open('theme.csv', 'w') as file:
        dict_writer = csv.DictWriter(file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(themes_list)
        
    return themes_list

def get_toys_pages(soup):
    n_toys = int(soup.select('span[data-value]')[0].get('data-value'))
    n_pages = n_toys // 18 + 1

    return n_pages, n_toys

def get_toys_values(collection='Marvel'):
    with open(file='index.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    
    toys = soup.find_all('li', {'data-test': 'product-item'})
    
    for toy in toys:
        toy_name = toy.find('h3').text
        print(toy_name)


def main():
    # soup = get_soup(url=url_themes)
    # themes = get_themes(soup=soup)
    
    # soup = get_soup(url='https://www.lego.com/en-us/themes/star-wars')
    # print(get_toys_pages(soup=soup))
    
    soup = get_soup(url='https://www.lego.com/en-us/themes/marvel')
    # get_toys_values(soup=soup)


if __name__== '__main__':
    main()
