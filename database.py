import logging
from link_shortener import Config
from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine(Config.DATABASE_URL,
                       pool_size=5,
                       max_overflow=10,
                       pool_timeout=30,
                       echo=True)

Session = scoped_session(sessionmaker(bind=engine))


def get_db():
    session = Session()
    try:
        yield session
    except (SQLAlchemyError, DatabaseError):
        raise DatabaseError
    finally:
        session.close()
        Session.remove()
