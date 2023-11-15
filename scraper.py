from bs4 import BeautifulSoup
import requests

URL = 'https://habr.com/ru/hubs/python/articles/'

results = requests.get(URL)
page = results.content

soup = BeautifulSoup(page, "html.parser")
articles = soup.find(class_="tm-articles-list").find_all('article',class_="tm-articles-list__item")
for article in articles:
    title = article.find(class_="tm-title__link")
    link = title['href']
    time = article.find(class_="tm-article-datetime-published").time
    time= time['title']
    print(f'https://habr.com{link}', title.text, time)