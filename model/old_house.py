# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 20:45
# @Author  : baiyoudong
# @File    : old_house.py

from sqlalchemy import Column, BIGINT, INT, VARCHAR, TEXT, FLOAT, DATETIME, text

from base import Base


class OldHouse(Base):
    __tablename__ = 'old_house'

    info_id = Column(BIGINT, primary_key=True, autoincrement=True)
    title = Column(TEXT, nullable=False)
    source = Column(INT, index=True)
    url = Column(VARCHAR(255), unique=True)
    city = Column(TEXT, nullable=False)
    district = Column(TEXT)
    house_name = Column(VARCHAR(255))
    house_type = Column(VARCHAR(255))
    description = Column(TEXT)
    total_price = Column(FLOAT, index=True)
    price_per_m = Column(FLOAT, index=True)
    update_time = Column(DATETIME, index=True)
    collect_time = Column(DATETIME, index=True, server_default=text('NOW()'))

