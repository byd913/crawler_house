# -*- coding: utf-8 -*-
# @Time    : 2017/6/22 15:36
# @Author  : baiyoudong
# @File    : publisher.py

from model.rent_house import Session


def publish(house_model):
    db_session = Session()
    db_session.add(house_model)
    db_session.commit()
    db_session.close()

