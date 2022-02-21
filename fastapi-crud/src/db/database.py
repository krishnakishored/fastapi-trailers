from config import Settings, get_settings
from sqlalchemy import create_engine, inspect, select
from sqlalchemy.exc import DBAPIError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy_utils import create_database, database_exists

settings: Settings = get_settings()

Base = declarative_base()

"""
application prerequisite:
    1. Create a Admin DB (what should be data in it?)
    1. create a user with privilege to create DBS (but access the system)
"""


def get_db_engine(db_name: str = settings.PG_DBNAME, create_db=False):
    """
    #TODO: create a db with PG_CONFIG passed
    """
    db_engine = None
    # SQLALCHEMY_DATABASE_URL = "sqlite:///./fastapi-practice.db"
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{settings.PG_DBUSER}:{settings.PG_DBPASS}"
        f"@{settings.PG_DBHOST}:{settings.PG_DBPORT}/{db_name}"
    )
    try:
        if create_db is not False and not database_exists(SQLALCHEMY_DATABASE_URL):
            create_database(SQLALCHEMY_DATABASE_URL)
    except (SQLAlchemyError, DBAPIError, OperationalError) as e:
        # TODO
        print("####################")
        print(e)
        print("####################")
        # TODO: handle it properly
    else:
        db_engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            pool_size=50,  # TODO: what's the ideal pool_size??
            echo=False,
            # connect_args={"check_same_thread": False}, // needed for SQLite
        )
    return db_engine


def get_db_session(db_name: str = settings.PG_DBNAME):
    """_summary_
    ## TODO: use a context manager and handle rollback
    Yields:
        _type_: _description_
    """

    engine = get_db_engine(db_name)

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
        # autocommit=False, autoflush=False, bind=get_engine_from_settings()
    )

    # Each instance of the SessionLocal class will be a database session.
    db = SessionLocal()
    try:
        # The yielded value is what is injected into path operations and other dependencies:
        yield db
    except (SQLAlchemyError, DBAPIError, OperationalError) as e:
        db.rollback()
        raise
    # The code following the yield statement is executed after the response has been delivered:
    finally:
        db.close()


def get_db_tables(db_name: str = settings.PG_DBNAME):
    sqlalchemy_inspector = inspect(get_db_engine(db_name))
    return sqlalchemy_inspector.get_table_names()


def get_pg_databases():
    """returns list of databases owned by user

    ## datname - The name of the database.
    ## datdba - The owner of the database, oid references pg_authid.oid.

    ## TODO: legacy methods in use (to be replaced)
    """

    engine = get_db_engine()

    # with engine.connect() as connection:
    with engine.begin() as connection:
        statement_1 = text(
            f"SELECT usesysid FROM pg_user WHERE usename='{settings.PG_DBUSER}'"
        )

        datdba_usesysid = connection.execute(statement_1).first()[0]
        print(datdba_usesysid)
        statement_2 = text(
            f"SELECT datname FROM pg_database WHERE datdba={datdba_usesysid}"
        )
        result = connection.execute(statement_2).all()
        database_list = [item[0] for item in result]
        return database_list


#     return db_list


if __name__ == "__main__":
    # session = get_db()
    # db_name = "example01"
    # list_of_tables = get_db_tables(db_name)
    # print(list_of_tables)
    list_of_databases = get_pg_databases()
    print(list_of_databases)
