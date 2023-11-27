from bs4 import BeautifulSoup
import requests
from utils import get_html
from app.articles.news import News
from sqlmodel import Session, select
from app.core.db_sync import engine


def scrape_article_text(article_url):
    html = get_html(article_url)
    soup = BeautifulSoup(html, "html.parser")
    article_text = soup.find("div", class_="article-formatted-body").decode_contents()
    return article_text


def save_news(article_title, article_url, publishing_time, article_content):
    with Session(engine) as session:
        query = select(News).where(News.url == article_url)
        news_exists = session.exec(query).all()
        if not news_exists:
            new_news = News(
                title=article_title,
                url=article_url,
                published=publishing_time,
                content=article_content,
            )
            session.add(new_news)
            session.commit()


URL = "https://habr.com/ru/hubs/python/articles/"

page = get_html(URL)

soup = BeautifulSoup(page, "html.parser")
articles = soup.find_all("article")
for article in articles:
    article_title = article.find(class_="tm-title__link")
    article_url = f'https://habr.com{article_title["href"]}'
    article_title = article_title.text
    publishing_time = article.find(class_="tm-article-datetime-published").time
    publishing_time = publishing_time["title"]
    article_content = scrape_article_text(article_url)
    # print(article_url, article_title, publishing_time, article_content)
    save_news(article_title, article_url, publishing_time, article_content)
