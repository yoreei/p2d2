#!/usr/bin/env python
# coding: utf-8
from sqlalchemy import create_engine
#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('mysql://mydeb:mydeb@localhost/satest', echo=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

def __repr__(self):
    return "<User(name='%s', fullname='%s', nickname='%s')>" % (
     self.name, self.fullname, self.nickname)
Base.metadata.create_all(engine)
