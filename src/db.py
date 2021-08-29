import functools
from contextlib import contextmanager
from functools import lru_cache

from sqlalchemy.future import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session, scoped_session
from sqlalchemy.orm.exc import (
    MultipleResultsFound as SQLAlchemyMultipleResultsFound,
    NoResultFound as SQLAlchemyNoResultFound,
)

from src.config import get_settings

Base = declarative_base()


@lru_cache
def get_engine():
    return create_engine(
        get_settings().database_uri,
        pool_pre_ping=True,
        # connect_args={"check_same_thread": False},
    )


def get_session_local():
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=get_engine()))()


def get_db():
    try:
        db = get_session_local()
        yield db
    finally:
        db.close()


@contextmanager
def transaction(db_session: Session):
    try:
        yield
        db_session.commit()
    except Exception:
        db_session.rollback()
        raise


class NoResultFound(Exception):
    ...


class MultipleResultsFound(Exception):
    ...


def not_found_converter(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyNoResultFound:
            raise NoResultFound
        except SQLAlchemyMultipleResultsFound:
            raise MultipleResultsFound

    return wrapper
