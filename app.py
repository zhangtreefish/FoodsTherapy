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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem, Condition, User, Base
# from imgurpython import ImgurClient # TODO:no module

engine = create_engine('sqlite:///restaurantmenuconditionuser.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

myFirstRestaurant = Restaurant(name='steam', description='all things steamed')
mySecondRestaurant = Restaurant(name='3Fs',description='that features fiber, fitness, and fluid')
myThirdRestaurant = Restaurant(name='Eden',description='out of your dream garden')
myFourthRestaurant = Restaurant(name='School Lunch', description='balanced lunch for the precious bodies and minds')
session.add(myFirstRestaurant)
session.add(mySecondRestaurant)
session.add(myThirdRestaurant)
session.add(myFourthRestaurant)
session.commit()
restaurant_list=session.query(Restaurant).all()
print session.query(Restaurant).first().name

# will not work if restaurant='myFirstRestaurant'
myFirstMenu = MenuItem(name='jade',
                       description='daikon steamed to a luscious texture',
                       price='$2.50',
                       course='vegetable',
                       restaurant=myFirstRestaurant)
mySecondMenu = MenuItem(name='fragrant snow',
                        description='sweet rice flour balls encasing honey-infused sweet olive blossoms and coconut oil',
                        price='$4.00',
                        course='dessert',
                        restaurant=myFirstRestaurant)
myThirdMenu = MenuItem(name='Four-layered dip',
                       description='organic black beans, avacado, tomato, cheese, dressed in lemon juice, srved with tortilla chips',
                       price='$4.00',
                       course='One Complete Meal',
                       restaurant=mySecondRestaurant)
myFourthMenu = MenuItem(name='chicken noodle soup',
                       description='what else can you say? made with carrots, celery, onion,garlic, tomato, zucchini, and ginger root',
                       price='$5.00',
                       course='One Complete Meal',
                       restaurant=myFourthRestaurant)
myFifthMenu = MenuItem(name='ocean',
                       description='soup made of tilapia,  celery, cilantro, green onion,garlic, tomato, zucchini, and ginger root',
                       price='$5.00',
                       course='One Complete Meal',
                       restaurant=myFourthRestaurant)
mySixthMenu = MenuItem(name='seaweed',
                       description='Wakame salad in green onion, hemp heart,sesame oil, and salt,served with two pieces of baked tofu, and a baked sweet potato',
                       price='$5.00',
                       course='One Complete Meal',
                       restaurant=mySecondRestaurant)
mySeventhMenu = MenuItem(name='ocean',
                       description='soup made of tilapia,  celery, cilantro, green onion,garlic, tomato, zucchini, and ginger root',
                       price='$5.00',
                       course='One Complete Meal',
                       restaurant=myFourthRestaurant)
session.add(myFirstMenu)
session.add(mySecondMenu)
session.add(myThirdMenu,myFourthMenu)
# session.add(myFourthMenu)
session.add(myFifthMenu)
session.add(mySixthMenu)
session.add(mySeventhMenu)
session.commit()
laRes = session.query(MenuItem).first().name
print laRes

myFirstCondition = Condition(name='diabetes',signs_and_symptoms='thirst, fatigue, frequent urination, weight loss')
mySecondCondition = Condition(name='gray hair',signs_and_symptoms='natural graying of hair')
session.add(mySecondCondition)
session.commit()
# link a menu to myFirstCondition
diabeticMenu1 = MenuItem(name='baked sweet potato',
                        description='sweet potato baked at 350 for 45 minutes, with skin',
                        price='$3.00',
                        course='vegetable',
                        restaurant=myFirstRestaurant)
session.add(diabeticMenu1)
session.commit()
myFirstCondition.suggested_menus.append(diabeticMenu1)
session.add(myFirstCondition)
session.commit()
firstCon = session.query(Condition).first()
print firstCon.name
# print firstCon.suggested_menus.count()  # TODO: why diabeticMenu1 not in the list?
 # to get image from imgur:
# client_id = '32dba864f458125'
# client_secret = 'YOUR CLIENT SECRET'
# client = ImgurClient(client_id,client_secret)
# img1='client.getAlbumImages(0)'
https://api.imgur.com/3/image/{id}
# img2='https://api.imgur.com/3/image/{id}'

# Example request
# items = client.gallery()
# for item in items:
#     print "pic-link:",item.link

myFirstUser = User(name='treefish',email='zhangtreefish@yahoo.com', picture='')
mySecondUser = User(name='bob',email='fearlessluke8@gmail.com', picture='http://i.imgur.com/3L3kK3q.png?1')

session.add(mySecondUser)
session.commit()
# The following unnecessary: the associations were already present, see project.py newMenu()
# myFirstUser.restaurants.append(myFirstRestaurant)
# myFirstUser.conditions.append(myFirstCondition)
# myFirstUser.menus.append(myFirstMenu)
# myFirstUser.menus.append(mySecondMenu)
session.add(myFirstUser)
session.commit()

from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
# import manyRestaurants

import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem, Condition, Base, User, engine

# New imports for state token
from flask import session as login_session
import random
import string

# import for new gconnect using verify_id_token API
from oauth2client import client, crypt

# IMPORTS FOR gconnect
from oauth2client.client import flow_from_clientsecrets  # creates a Flow object from a client_secrets.json file
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests # Requests is an Apache2 Licensed HTTP library, written in Python, for human beings.

# for RSS feed endpoint
# import feedparser

# for xml endpoint
# from dict2xml import dict2xml as xmlify
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom

# from Facebook OAuth 2 Tutorial
# from requests_oauthlib import OAuth2Session
# from requests_oauthlib.compliance_fixes import facebook_compliance_fix

# if just do 'from manyRestaurants import Restaurant, session' and without the next 4 lines,get error
# 'SQLite objects created in a thread can only be used in that same thread'
engine = create_engine('sqlite:///restaurantmenuconditionuser.db',echo=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

G_CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']

APPLICATION_NAME = "Therapeutic Foods Restaurants"

# for heroku

# TODO:Here I attempted adding id init, but had to remove: 'IntegrityError: (IntegrityError) UNIQUE constraint failed'
def createUser(login_session):
    """generator of user if the user is in session(i.e. logged in)"""

    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture']
                   # id=login_session['user_id']
                   )
    session.add(newUser)
    session.commit()
    # user=session.query(User).filter_by(email=login_session['email']).one() # TODO: multiple rows were found for one()
    user=session.query(User).filter_by(email=login_session['email']).first()
    print user.name
    return user.id

def getUserInfo(user_id):
    """identifying the user with certain user_id"""

    user = session.query(User).filter_by(id=user_id).one()
    print "user:",user
    return user

def getUserId(email):
    """identifying the user_id with the user's email"""

    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# The server creates anti-forgery state token and sends to the client
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template("login.html", STATE=state)


@app.route('/login2/')
def showLoginTwo():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template("login2.html", STATE=state)

@app.route('/login3/')
def showLogin3():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template("login3.html", STATE=state)

@app.route('/login4/')
def showLoginFour():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template("login4.html", STATE=state)

@app.route('/login5/')
def showLoginFive():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template("login5.html", STATE=state)

@app.route('/gconnect/', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']: # check what client sent is what server sent
        return jsonify(message='Invalid state parameter.'),401
    # Obtain the one-time authorization code from authorization server
    code = request.data
    print 'code'
    print code

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='', # creates a Flow object from a client_secrets.json file
                                             redirect_uri = 'postmessage')
        credentials = oauth_flow.step2_exchange(code)  # exchanges an authorization code for a Credentials object
    except FlowExchangeError:
        return jsonify(message='Failed to upgrade the authorization code.'), 401

    # Check that the access token is valid.
    # A Credentials object holds refresh and access tokens that authorize access
    # to a single user's data. These objects are applied to httplib2.Http objects to
    # authorize access.
    print credentials
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1]) # loads:Deserialize to a Python object
    print "result:",result
    # If there was an error in the access token info, abort.
    # dict.get(key, default=None)
    # The method get() returns a value for the given key. If key unavailable then returns default None.
    if result.get('error') is not None:
        # response = make_response(json.dumps(result.get('error')), 500)
        # response.headers['Content-Type'] = 'application/json'
        return jsonify(message=result.get('error')),500



    # Verify that the access token is used for the intended user.
    # id_token: object, The identity of the resource owner.
    # 'Google ID Token's field (or claim) 'sub' is unique-identifier key for the user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps
            ("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        return jsonify(message="Token's user ID doesn't match given user ID."),401

    # Verify that the access token is valid for this app.
    if result['issued_to'] != G_CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
        return jsonify(message="Token's client ID does not match app's."),401


    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        # response = make_response(json.dumps('Current user is already connected.'),
        #                          200)
        # response.headers['Content-Type'] = 'application/json'
        # return response
        return jsonify(message='Current user is already connected.'),200

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id
    login_session['access_token'] = credentials.access_token

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # check to see if user exist
    # user = session.query(User).one()
    # if user is None:
    #     createUser(login_session)
    # print user.name
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, User'
    output += str(login_session['user_id'])
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '">'
    # output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'],'message')
    print "done gconnect!"
    return output


@app.route('/gdisconnect/')
def gdisconnect():  # TODO: put on login.html?
    # Only a connected user
    print 'login_session:',login_session
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        # (can also be:) return jsonify(message='Why, current user not connected.'),401

    # Execute HTTP GET request to revoke current token
    access_token = credentials.access_token
    print 'access_token:',access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')
    print 'gdisconnect request result:', result
    print "login_session['username'] before del:",login_session['username']
    if result[0]['status'] == 200:  # TODO: why 200 means to clear cache while '200' not
        # Reset the user's session
        del login_session['credentials']
        del login_session['gplus_id']

        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']
        del login_session['user_id']
        print "login_session['username'] after del:",login_session['username']
        # response = make_response(json.dumps('User successfully disconnected.'), 200)
        # response.headers['Content-Type'] = 'application/json'
        # return  response
        return jsonify(message='User successfully disconnected.'), 200
    else:
        # response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        # response.headers['Content-Type'] = 'application/json'
        # return response
        return jsonify(message='Failed to revoke token for given user.'), 400


@app.route('/fbconnect/', methods=['POST'])
def fbconnect():
    # Validate state token
    print request.args.get('state')
    print login_session['state']
    if request.args.get('state') != login_session['state']: # check what client sent is what server sent
        response = make_response(json.dumps('Invalid state parameter.'), 401)  #dumps:Serialize obj to a JSON formatted str
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain the one-time authorization code from authorization server
    access_token = request.data

    print 'fb access_token:',access_token  # works

    # try:
    #     # Upgrade the authorization code into a credentials object
    #     oauth_flow = flow_from_clientsecrets('fb_client_secrets.json', scope='', # creates a Flow object from a client_secrets.json file
    #                                          redirect_uri = 'postmessage')
    #     credentials = oauth_flow.step2_exchange(code)  # exchanges an authorization code for a Credentials object
    # except FlowExchangeError:
    #     response = make_response(
    #         json.dumps('Failed to upgrade the authorization code.'), 401)
    #     response.headers['Content-Type'] = 'application/json'
    #     return response

    # Check that the access token is valid.
    # A Credentials object holds refresh and access tokens that authorize access
    # to a single user's data. These objects are applied to httplib2.Http objects to
    # authorize access.
    # print 'credentials'
    # print credentials

    app_info = json.loads(open('fb_client_secrets.json','r').read())
    # print app_info.to_json() # why print not working?
    app_id = app_info['web']['app_id']
    app_secret = app_info['web']['app_secret']
    print "app param:",app_id, app_secret
    token_url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id,app_secret,access_token)
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    # token_url1 ='https://graph.facebook.com/v2.5/oauth/access_token?\
    #             client_id=%s&\
    #             client_secret=%s&\
    #             code=%s'(app_id,app_secret,access_token)
    # redirect_uri = 'http://localhost:5000/'
    # facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
    # facebook = facebook_compliance_fix(facebook)
    # access_token = facebook.fetch_token(token_url, client_secret=client_secret)
    # print 'Please go here and authorize,', authorization_url


    h = httplib2.Http()
    # result = json.loads(h.request(token_url, 'GET')[1]) # loads:Deserialize to a Python object
    result = h.request(url, 'GET')[1]

    # try imgur
    h = httplib2.Http()
    imgru_url = 'https://api.imgur.com/3/album/0/images'
    img_result = h.request(url, 'GET')[1]
    print 'IMAGE:', img_result

    # result = h.request(token_url, 'GET')[1]
    # print 'result:',result # TODO nothign
    token = result.split("&")[0]
    print 'the token:',token

    # url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    info_url = 'https://graph.facebook.com/v2.5/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    data=json.loads(h.request(info_url, 'GET')[1])
    print "data:", data

    login_session['provider'] = 'facebook'
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']

    pic_url = 'https://graph.facebook.com/v2.5/me/picture?%s&redirect=0' % token
    h = httplib2.Http()
    pic = json.loads(h.request(pic_url, 'GET')[1])
    print "pic",pic
    login_session['picture'] = pic['data']['url']

    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, User'
    output += str(login_session['user_id'])
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '">'
    # output += ' " style = "width: 100px; height: 100px;border-radius: 50px;-webkit-border-radius: 50px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'],'message')
    print "done via FB!"
    return output

@app.route('/fbdisconnect/')
def fbdisconnect():  # TODO: put on login.html?

    # Execute HTTP GET request to revoke current token
    facebook_id = login_session['facebook_id']
    url = 'https://accounts.google.com/%s/permissions' % facebook_id
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[0] # TODO

    if result['status'] == 200:  # TODO: why 200 means to clear cache while '200' not
        # Reset the user's session
        del login_session['facebook_id']
        del login_session['user_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        # response = make_response(json.dumps('User successfully disconnected.'), 200)
        # response.headers['Content-Type'] = 'application/json'
        # return  response
        return jsonify(message='User successfully disconnected from FB.'), 200
    else:
        # response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        # response.headers['Content-Type'] = 'application/json'
        # return response
        return jsonify(message='Failed to revoke token for given user.'), 400

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.","message")
        return redirect(url_for('showRestaurants'))
    else:
        flash("You were not logged in","message")
        return redirect(url_for('showRestaurants'))

# @app.route('/disconnect/')
# def disconnect():
#     if 'provider' in login_session:
#         if login_session['provider'] == 'google': #TODO: why not work?
#             gdisconnect()
#             return redirect(url_for('gdisconnect'))
#         elif login_session['provider'] == 'facebook':
#             return redirect(url_for('fbdisconnect'))
#     else:
#         flash('You are not logged in to begin with!','message')
#         return redirect(url_for('showRestaurants'))

@app.route('/restaurants/JSON/')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurant=[i.serialize for i in restaurants])

@app.route('/restaurants/RSS/')
def restaurantsRSS():
    d = feedparser.parse()
    print d.feed.title

# for use in restaurantsXml()
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

@app.route('/restaurants/xml/')
def restaurantsXml():
    restaurants = session.query(Restaurant).all()
    top = Element('top')
    for r in restaurants:
        child = SubElement(top, 'child')
        child.text = r.name
        child2 = SubElement(top, 'child')
        child2.text = '\n' # TODO: insert newline
    return prettify(top)
    # restaurants = session.query(Restaurant).all()
    # restaurantsJSON = jsonify(restaurant=[i.serialize for i in restaurants])
    # return xmlify(restaurantsJSON, wrap="all", indent="  ")


@app.route('/restaurants/')
def showRestaurants():
    try:
        restaurants = session.query(Restaurant).all()
        # if login_session['user_id'] == owner_id : TODO: why this line cause [KeyError: 'user_id']
        if login_session.get('user_id') is None:
            return render_template('restaurantsPublic.html', restaurants=restaurants)
        else:
            owner = getUserInfo(createUser(login_session)) #aha! This addressed 'username' error
            return render_template('restaurants.html', restaurants=restaurants,user=owner)
    except IOError as err:
        return "No restaurant, error:"
    finally:
        flash("This page will show all my restaurants","message")

@app.route('/restaurants/new/', methods=['POST','GET'])
def restaurantNew():
    if request.method == 'POST':
        myNewRestaurant = Restaurant(name=request.form['newName'],
                                     description=request.form['newDescription'],
                                     user_id=login_session['user_id'])
        session.add(myNewRestaurant)
        session.commit()
        flash('New restaurant ' + myNewRestaurant.name+' has been created!','message')
        return redirect(url_for('showRestaurants'))
    else:
        if login_session.get('username') is None:
            return redirect(url_for('showLogin'))
        else:
            owner = createUser(login_session)
            return render_template('newRestaurant.html',user=owner)

@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['POST','GET'])
def restaurantEdit(restaurant_id):
    if request.method == 'POST':
        laRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        laRestaurant.name = request.form['newName']
        session.add(laRestaurant)
        session.commit()
        flash('The restaurant '+ laRestaurant.name+ ' has been edited!','message')
        return redirect(url_for('showRestaurants'))
    else:
        if login_session.get('username') is None:
            return redirect(url_for('showLogin'))
        laRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template('editRestaurant.html', restaurant_id=restaurant_id,restaurant=laRestaurant)

@app.route('/restaurants/<int:restaurant_id>/delete/',methods=['POST','GET'])
def restaurantDelete(restaurant_id):
    laRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if login_session.get('username') is None:
        return redirect(url_for('showLogin'))
    if login_session['user_id'] != laRestaurant.user_id:
        return render_template('notAuthorized.html')
    if request.method == 'POST':
        if(laRestaurant):
            session.delete(laRestaurant)
            session.commit()
            flash('Restaurant '+laRestaurant.name+' has been sadly deleted...','message')
            return redirect(url_for('showRestaurants'))
        else:
            return "no such restaurant found"  # TODO: send error message when no such restaurant
    else:
        return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, restaurant=laRestaurant)


@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    menus = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return jsonify(menuItem=[i.serialize for i in menus])

@app.route('/menus/JSON/')
def allMenusJSON():
    menus = session.query(MenuItem).order_by(MenuItem.id)
    return jsonify(menuItem=[i.serialize for i in menus])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuJSON(restaurant_id, menu_id):
    menu = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(menuItem=menu.serialize)


# route() decorator to tell Flask what URL should trigger method

@app.route('/', defaults={'restaurant_id': 1}) # if w/o default,do as so: showMenus(restaurant_id=1):
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenus(restaurant_id):
    try:
        # without one(), gets error 'AttributeError: 'Query' object has no attribute 'id''
        laRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        myMenus = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
        # owner = getUserInfo(laRestaurant.user_id)
        # print "owner:",owner
        if login_session.get('username') is None or laRestaurant.user_id != login_session['user_id']:
            return render_template('menuPublic.html', restaurant=laRestaurant, menus=myMenus)
        else:
            return render_template('menu.html', restaurant=laRestaurant, menus=myMenus)
    except IOError as err:
        return "No menus available yet."

# @app.route('/')
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenu(restaurant_id):
    if request.method == 'POST':
        laRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        myNewMenu = MenuItem(name=request.form['newName'],
                             course=request.form['newCourse'],
                             description=request.form['newDescription'],
                             price=request.form['newPrice'],
                             restaurant_id=restaurant_id,
                             user_id=laRestaurant.user_id)
        myNewCondition = Condition(name=request.form['newConditions'])
        session.add(myNewCondition)
        myNewMenu.conditions.append(myNewCondition)
        session.add(myNewMenu)
        session.commit()
        flash('New menu ' + myNewMenu.name+' has been created!','message')
        return redirect(url_for('showMenus',restaurant_id=restaurant_id))
    else:
        if login_session.get('username') is None:
            return redirect(url_for('showLogin'))
        laRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template('newMenuItem.html',restaurant_id=restaurant_id, restaurant=laRestaurant)

# Task 2: Create route for editMenuItem function here TODO

# @app.route('/')
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenu(restaurant_id, menu_id):
    laMenu = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        laMenu.name = request.form['newName']
        laMenu.course = request.form['newCourse']
        laMenu.description = request.form['newDescription']
        laMenu.price = request.form['newPrice']
        session.add(laMenu)
        session.commit()
        flash('The menu '+laMenu.name + ' has been edited!','message')
        return redirect(url_for('showMenus',restaurant_id=restaurant_id))
    else:
        if login_session.get('username') is None:
            return redirect(url_for('showLogin'))
        laRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id,restaurant=laRestaurant, menu=laMenu)

# @app.route('/')
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenu(restaurant_id, menu_id):
    laMenu = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        name =  laMenu.name
        session.delete(laMenu)
        session.commit()
        flash('the menu '+name+' has been deleted!','message')
        return redirect(url_for('showMenus',restaurant_id=restaurant_id))
    else:
        if login_session.get('username') is None:
            return redirect(url_for('showLogin'))
        return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, menu=laMenu)

@app.route('/conditions/')
def showConditions():
    try:
        conditions = session.query(Condition).all()
        if login_session.get('user_id') is None:
            return render_template('conditionsPublic.html', conditions=conditions)
        else:
            owner = getUserInfo(createUser(login_session)) #aha! This addressed 'username' error
            return render_template('conditions.html', conditions=conditions,user=owner)

    except IOError as err:
        return "No conditions, error:"
    finally:
        flash("This page shows all conditions...","message")

@app.route('/conditions/new/', methods=['POST','GET'])
def newCondition():
    if request.method == 'POST':
        condition = Condition(name=request.form['name'],
                              signs_and_symptoms=request.form['signs_and_symptoms'],
                              user_id=login_session['user_id']
                              )
        session.add(condition)
        session.commit()
        flash('the condition '+condition.name+' has been listed!','message')
        return redirect(url_for('showConditions'))
    else:
        if login_session.get('username') is None:
            return redirect(url_for('showLogin'))
        return render_template('newCondition.html')


@app.route('/conditions/<int:condition_id>/edit', methods=['POST','GET'])
def conditionEdit(condition_id):
    laCondition = session.query(Condition).filter_by(id=condition_id).one()
    if request.method == 'POST':
        laCondition.name = request.form['newName']
        laCondition.signs_and_symptoms = request.form['newSignsAndSymptoms']
        session.add(laCondition)
        session.commit()
        flash('the condition '+laCondition.name+' has been edited!','message')
        return redirect(url_for('showConditions'))
    else:
        if login_session.get('username') is None:
            return redirect(url_for('showLogin'))
        return render_template('editCondition.html',condition_id=condition_id,condition=laCondition)

@app.route('/conditions/<int:condition_id>/delete',methods=['POST','GET'])
def conditionDelete(condition_id):
    laCondition = session.query(Condition).filter_by(id=condition_id).one()
    if request.method == 'POST':
        session.delete(laCondition)
        flash('the condition '+laCondition.name+' has been deleted!','message')
        return redirect(url_for('showConditions'))
    else:
        if login_session.get('username') is None:
            return redirect(url_for('showLogin'))
        return render_template('deleteCondition.html',condition_id=condition_id,condition=laCondition)

@app.route('/conditions/<int:condition_id>/menu/')
def conditionMenus(condition_id):
    laCondition = session.query(Condition).filter_by(id=condition_id).one()
    menus = laCondition.suggested_menus
    return render_template('conditionMenus.html', condition_id=condition_id,condition=laCondition, menus=menus)

# this method allows to add a menu suitable for certain condition to a restaurant
@app.route('/conditions/<int:condition_id>/new/', methods=['GET','POST'])
def newConditionMenu(condition_id):
    if request.method == 'POST':
        laCondition = session.query(Condition).filter_by(id=condition_id).one()
        laRestaurant_id = session.query(Restaurant).filter_by(name=request.form['newRestaurantName']).one().id
        newConditionMenu = MenuItem(name=request.form['newName'],
                             course=request.form['newCourse'],
                             description=request.form['newDescription'],
                             price=request.form['newPrice'],
                             restaurant_id=request.form['newRestaurantId'],
                             user_id=login_session['user_id'])
        newConditionMenu.conditions.append(laCondition)
        # laCondition.suggested_menus.append(newConditionMenu)
        session.add(newConditionMenu)
        # session.add(laCondition)
        session.commit()
        flash('New menu ' + newConditionMenu.name+' has been created!','message')
        return redirect(url_for('conditionMenus',condition_id=condition_id))
    else:
        if login_session.get('username') is None:
            return redirect(url_for('showLogin'))
        laCondition = session.query(Condition).filter_by(id=condition_id).one()
        restaurants = session.query(Restaurant).all()
        return render_template('newConditionMenu.html',condition_id=condition_id, condition=laCondition,restaurants=restaurants)

if __name__ == '__main__':
    # TODO: set to False before deployment: enable debug so the server reloads itself on code changes
    app.secret_key='super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
