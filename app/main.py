import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel, Session, select

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
def get_news():
    with Session(engine) as session:
        newss = session.exec(select(News)).all()
        return newss


@app.post("/news/", response_model=News)
def post_news(news: News):
    with Session(engine) as session:
        session.add(news)
        session.commit()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True)
