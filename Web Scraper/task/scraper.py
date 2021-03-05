import requests
import json
from bs4 import BeautifulSoup
import string
import os

art = []
link = []

number_of_pages = int(input())
type_of_articles = input()
dir = os.getcwd()
for cycle in range(1, number_of_pages + 1):

    try:
        os.mkdir(f'Page_{cycle}')
    except FileExistsError:
        pass
    os.chdir(dir + f'\\Page_{cycle}')
    r = requests.get(f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={cycle}')
    if r.status_code == 200:
        data = BeautifulSoup(r.content, 'html.parser')
        tag_news = data.find_all('article')   # data.find_all('span', {'data-test': 'article.type'})

        for i in tag_news:
            if i.find('span', class_='c-meta__type').text == type_of_articles:
                link = "https://www.nature.com" + i.find('a', {"data-track-action": "view article"}).get("href")

                new_article = requests.get(link)

                article = BeautifulSoup(new_article.content, 'html.parser')
                try:
                    article_title = article.find('h1', {'class': 'article-item__title'}).text
                except AttributeError:
                    article_title = article.find('h1', {'class': 'c-article-title'}).text

                outtab = "_" * 32
                intab= string.punctuation
                trantab = str.maketrans(intab, outtab)

                article_title = article_title.translate(trantab)

                article_title = article_title.replace('_', '')
                article_title = article_title.replace(' ', '_')
                try:
                    article_body = article.find('div', {'class': 'article__body'}).text
                except AttributeError:
                    try:
                        article_body = article.find('div', {'class': 'c-article-section__content'}).text
                    except AttributeError:
                        article_body = article.find('div', {'class': 'article-item__body'}).text
                article_body = article_body.strip()
                with open(article_title + '.txt', 'wb') as file:
                    file.write(str.encode(article_body))
    os.chdir(dir)
