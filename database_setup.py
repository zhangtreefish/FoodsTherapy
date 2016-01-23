#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# TODO:user:restaurant is one: many; user:condition is one:many or many:many?; user:menu is there relationship?
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    email = Column(String(30))
    picture = Column(String(30))
    restaurants = relationship('Restaurant', back_populates='user') # TODO:more rels
    conditions = relationship('Condition', back_populates='user')
    menus = relationship('MenuItem',back_populates='user')


# restaurant:menu  is one:many;condition:menu is many:many;
class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    # column 'name' is mapped to the 'name' attribute of class 'Restaurant'
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    menus = relationship('MenuItem',back_populates='restaurant')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User',back_populates='restaurants')

    def __repr__(self):
        return "<Restaurant(name='%s', description='%s')>" % (
                             self.name, self.description)

    @property
    def serialize(self):
        return {'name':self.name,
                'description':self.description,
                'id':self.id,
                'user_id':self.user_id
                }

condition_menu = Table('condition_menu',Base.metadata,
                          Column('condition_id', Integer, ForeignKey('condition.id')),
                          Column('menu_id', Integer, ForeignKey('menu_item.id'))
                          )


class Condition(Base):
    __tablename__ = 'condition'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    signs_and_symptoms = Column(String(250))
    suggested_menus = relationship('MenuItem',secondary=condition_menu, back_populates='conditions')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='conditions')

class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship('Restaurant', back_populates='menus')
    conditions = relationship('Condition', secondary=condition_menu, back_populates='suggested_menus')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='menus')

# Restaurant.menu_item = relationship('MenuItem',order_by=MenuItem.id,back_populates='restaurant')

    @property
    def serialize(self):
        return {'name':self.name,
                'course':self.course,
                'description':self.description,
                'price':self.price,
                'id':self.id,
                'restaurant_id':self.restaurant_id,
             #    'condition_id':self.condition_id
             #   'restaurant':self.restaurant  # 'restaurant is not serializable'
                }

# issue CREATE statements for all tables using MetaData object created during declarative_base()
engine = create_engine('sqlite:///restaurantmenuconditionuser.db', echo=True)
Base.metadata.create_all(engine)
