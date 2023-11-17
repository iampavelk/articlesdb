from bs4 import BeautifulSoup
import requests


def scrape_article_text(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.content, "html.parser")
    article_text = soup.find("div", class_="article-formatted-body")
    return article_text


URL = "https://habr.com/ru/hubs/python/articles/"

results = requests.get(URL)
page = results.content

soup = BeautifulSoup(page, "html.parser")
articles = soup.find_all("article")
for article in articles:
    article_title = article.find(class_="tm-title__link")
    article_url = f'https://habr.com{article_title["href"]}'
    publishing_time = article.find(class_="tm-article-datetime-published").time
    publishing_time = publishing_time["title"]
    article_content = scrape_article_text(article_url)
    print(article_url, article_title.text, publishing_time, article_content)
    break
