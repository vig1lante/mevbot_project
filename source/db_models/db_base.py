from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Enum, select, func, and_
import enum

Base = declarative_base()

class ABIs(Base):
    __tablename__ = 'abis'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, index=True)
    net = Column(String, index=True)
    abi = Column(String)
