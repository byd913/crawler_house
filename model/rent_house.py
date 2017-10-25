# -*- coding: utf-8 -*-
# @Time    : 2017/6/22 15:04
# @Author  : baiyoudong
# @File    : rent_house.py
from sqlalchemy import Column, BIGINT, INT, VARCHAR, TEXT, FLOAT, DATETIME, text

from base import Base


class RentHouse(Base):
    __tablename__ = 'rent_house'

    info_id = Column(BIGINT, primary_key=True, autoincrement=True)
    title = Column(TEXT, nullable=False)
    source = Column(INT, index=True)
    url = Column(VARCHAR(255), unique=True)
    city = Column(TEXT, nullable=False)
    district = Column(TEXT)
    house_name = Column(VARCHAR(255))
    house_type = Column(VARCHAR(255))
    rent_type = Column(VARCHAR(255), index=True)
    description = Column(TEXT)
    price = Column(FLOAT, index=True)
    update_time = Column(DATETIME, index=True)
    collect_time = Column(DATETIME, index=True, server_default=text('NOW()'))


if __name__ == '__main__':
    Base.metadata.create_all()
