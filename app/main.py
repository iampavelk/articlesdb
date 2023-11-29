import uvicorn
from fastapi import FastAPI, Request
from sqlalchemy.orm import load_only
from sqlmodel import SQLModel, Session, select
from fastapi.templating import Jinja2Templates

from app import settings
from app.core.models import HealthCheck
from app.articles.news import News
from app.core.db_sync import engine


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    debug=settings.debug,
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/front/templates")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/", response_model=HealthCheck, tags=["status"])
def health_check():
    return {
        "name": settings.project_name,
        "version": settings.version,
        "description": settings.description,
    }


@app.get("/news/")
def get_news(request: Request):
    with Session(engine) as session:
        news = session.exec(
            select(News).options(load_only(News.title, News.url, News.published))
        ).first()
        print(news.title, type(news))
        return templates.TemplateResponse(
            "news.html",
            context={
                "request": request,
                "title": news.title,
                "url": news.url,
                "published": news.published,
            },
        )


@app.post("/news/", response_model=News)
def post_news(news: News):
    with Session(engine) as session:
        session.add(news)
        session.commit()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True)
