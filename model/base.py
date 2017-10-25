# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 20:44
# @Author  : baiyoudong
# @File    : base.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from crawl_mysql_conf import *

data_base_uri = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % (
    MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE)
engine = create_engine(data_base_uri, echo=False, pool_size=10, pool_recycle=60)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
my_session = scoped_session(Session)

Base = declarative_base()
Base.metadata.bind = engine
