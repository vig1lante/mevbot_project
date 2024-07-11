import enum
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Enum, select, func, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from service_settings import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB_NAME
from sqlalchemy_utils import database_exists, create_database
from .db_models.db_base import ABIs, Base
import inspect

class PostgresDriver:
    def __init__(self):
        login = POSTGRES_USER
        password = POSTGRES_PASSWORD
        host = POSTGRES_HOST
        port = POSTGRES_PORT
        database_name = POSTGRES_DB_NAME
        db_url = f'postgresql+psycopg2://{login}:{password}@{host}:{port}/{database_name}'
        table_names = [ABIs]
        engine = create_engine(db_url)
        if not database_exists(engine.url):
            create_database(engine.url)
            Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)
        if not database_exists(engine.url):
            raise Exception(f"Database {engine.url} was not founded.")
        for table in table_names:
            if not sqlalchemy.inspect(engine).has_table(table.__tablename__):
                raise Exception(f"Table {table.__tablename__} was not founded in database.")

    def insert_data(self, data):
        session = self.session(expire_on_commit=False)
        try:
            session.add(data)
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(f"PostgresDriver error in {inspect.currentframe().f_code.co_name}() function. Error - {str(e)}")
        finally:
            session.close()

    def insert_bulk_data(self, data):
        session = self.session()
        try:
            session.bulk_save_objects(data)
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(f"PostgresDriver error in {inspect.currentframe().f_code.co_name}() function. Error - {str(e)}")
        finally:
            session.close()

    def get_all_abis(self, *args):
        session = self.session()
        try:
            data = session.query(ABIs).filter(*args).all()
        except Exception as e:
            raise Exception(
                f"PostgresDriver error in {inspect.currentframe().f_code.co_name}() function. Error - {str(e)}")
        finally:
            session.close()
        return data

    def get_first_abi(self, *args):
        session = self.session()
        try:
            data = session.query(ABIs).filter(*args).first()
        except Exception as e:
            raise Exception(
                f"PostgresDriver error in {inspect.currentframe().f_code.co_name}() function. Error - {str(e)}")
        finally:
            session.close()
        return data

    def exists_abi(self, *args):
        session = self.session()
        try:
            data = session.query(ABIs).filter(*args).first()
        except Exception as e:
            raise Exception(
                f"PostgresDriver error in {inspect.currentframe().f_code.co_name}() function. Error - {str(e)}")
        finally:
            session.close()
        return data is not None

    def update_abi(self, abi, *args):
        session = self.session()
        try:
            data = session.query(ABIs).filter(*args).first()
            if data is None:
                return False
            data.abi = abi
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(f"PostgresDriver error in {inspect.currentframe().f_code.co_name}() function. Error - {str(e)}")
        finally:
            session.close()
        return True
