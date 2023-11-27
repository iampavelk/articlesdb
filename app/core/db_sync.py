from sqlmodel import create_engine


from app import settings

engine = create_engine(settings.db_sync_connection_str, echo=True)
