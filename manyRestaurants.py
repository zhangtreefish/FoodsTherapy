from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem, Condition, User, Base, engine
import json
import logging
import imgur_secret
from imgurpython import ImgurClient
from auth import authenticate
from datetime import datetime


# access menu images in the app author's menu album (id 'risa2')at imgur.com
client = authenticate()
ids = client.get_account_album_ids('Zhangtreefish')
for a in ids:
    print 'album:',a
    images = client.get_album_images(a)
    for i in images:
        print 'itme list;', i.id,i.link, i.name
album_id = 'risa2'
print "album_id:!!!!!!!!!!", album_id
images = client.get_album_images(album_id)
for i in images:
    print 'itme list;', i.id,i.link

# sessionmaker: a session factory generator (in other words, a function
# that returns a function that returns a new Session for each call)
DBSession = sessionmaker(bind=engine)
# Session: a container of instances of mapped classes
session = DBSession()

data1 = {
    "restaurants": [
        {"name":"Steam", "description":"all things steamed"},
        {"name":'3Fs', "description":'that features fiber,fitness, and fluid'},
        {"name":'Eden', "description":'out of your dream garden'},
        {"name":'School Lunch',
        "description":"balanced lunch for the precious bodies and minds"}
    ]
}


def populate(restaurant):
    """ populate a single restaurant, skip if already present"""
    if session.query(Restaurant).filter_by(name=restaurant["name"]).first() is None:
        restaurant = Restaurant(name=restaurant["name"], description=restaurant["description"])
        session.add(restaurant)
        session.commit()
    else:
        return "Restaurant"+ restaurant + " already present."


def populateRestaurants(restaurants):
    """ to populate a list of restaurants, skip if already present"""
    try:
        for i in range(len(restaurants)):
            rest = session.query(Restaurant).filter_by(name=restaurants[i]["name"]).first()
            if rest is None:
                restaurant = Restaurant(name=restaurants[i]["name"], description=restaurants[i]["description"])
                session.add(restaurant)
            session.commit()
    except:
        return "Error: no restaurant is created."


# populate the restaurants
populateRestaurants(data1["restaurants"])
restaurant_num = session.query(Restaurant).count()
# print 'number of restaurants populated:', restaurant_num

myFirstRestaurant = session.query(Restaurant).filter_by(name="Steam").first()
mySecondRestaurant = session.query(Restaurant).filter_by(name="3Fs").first()
myThirdRestaurant = session.query(Restaurant).filter_by(name="Eden").first()
myFourthRestaurant = session.query(Restaurant).filter_by(name="School Lunch").first()
# print "second:", mySecondRestaurant

data2 = {
    "menus": [
        {"name": "Jade", "description": "daikon steamed to a luscious \
         texture", "price": "$2.50", "course": "vegetable",
         "restaurant": myFirstRestaurant},
        {"name":"fragrant snow", "description": "sweet rice flour balls \
         encasing honey-infused sweet olive blossoms and coconut oil",
         "price":"$4.00", "course": "dessert", "restaurant":
         myFirstRestaurant},
        {"name":"Four-layered dip", "description": "organic black beans,\
         avacado, tomato, cheese, dressed in lemon juice, served with \
         tortilla chips", "price":"$4.00", "course":"One Complete Meal",
         "restaurant": myThirdRestaurant},
        {"name":"chicken noodle soup", "description":"what else can you say? \
         made with carrots, celery, onion,garlic, tomato, zucchini, and \
         ginger root", "price": "$5.00", "course": "One Complete Meal",
         "restaurant":myFourthRestaurant},
        {"name":'seaweed', "description":"Wakame salad in green onion, hemp \
        heart, sesame oil, and salt,served with two pieces of baked tofu,\
         and a baked sweet potato", "price": "$5.00", "course": "One Complete\
          Meal", "restaurant": mySecondRestaurant},
        {"name":"ocean", "description":"soup made of tilapia,  celery, cilantro,\
        green onion,garlic, tomato, zucchini, and ginger root","price":
        "$5.00", "course":"One Complete Meal", "restaurant":
        myFourthRestaurant},
        {"name":"baked sweet potato", "description":"sweet potato baked at \
        350 for 45 minutes, with skin", "price":"$3.00", "course":
        "vegetable", "restaurant": mySecondRestaurant},
        {"name":"garlic chive", "description":"garlic chive chopped and stir-fried \
        with tofu, a traditional dish for problem of constipation", "price":"$3.00",
        "course": "vegetable", "restaurant": mySecondRestaurant}
    ]
}


def populateMenus(menus):
    """ method to populate a list of menus, skip if already present"""
    try:
        for i in range(len(menus)):
            if session.query(MenuItem).filter_by(name=menus[i]["name"]).first() is None:
                menu = MenuItem(name=menus[i]["name"],
                                description=menus[i]["description"],
                                price=menus[i]["price"],
                                course=menus[i]["course"],
                                restaurant=menus[i]["restaurant"])
                session.add(menu)
            session.commit()
    except:
        return "Error: no menu is created."


# populate the menus
populateMenus(data2['menus'])
menu_no = session.query(MenuItem).count()
# print 'menu number:', menu_no


data3 = {
    "conditions": [
        {"name": "diabetes", "signs_and_symptoms": "thirst, fatigue, frequent \
        urination, weight loss"},
        {"name": "gray hair", "signs_and_symptoms": "natural graying of hair"}
    ]
}


def populateConditions(conditions):
    """ method to populate a list of conditions, skip if already present"""
    try:
        for i in range(len(conditions)):
            if session.query(Condition).filter_by(name=conditions[i]["name"]).first() is None:
                condition = Condition(name=conditions[i]["name"],
                                      signs_and_symptoms=conditions[i]["signs_and_symptoms"],
                                      user_id="")
                session.add(condition)
            session.commit()
    except:
        return "Error: no condition is created."

def addMenuImage(menu_name, image_id):
    """
    assign a menu image from app author's imgur album to the image attribute
    of a menu item
    """
    try:
        menu = session.query(MenuItem).filter_by(name=menu_name).first()
        print "menu:", menu.name

        # access image in the album
        images = client.get_album_images(album_id)
        img_link = None
        for i in images:
            if i.id==image_id:
                img_link = i.link

        menu.image = img_link
        print "link:", menu_image
        session.add(menu)
        session.commit()
    except:
        return "Error: no image is added."


addMenuImage("Jade","ruIj52U") # ruIj52U
addMenuImage("garlic chive", "3L3kK3q") # 3L3kK3q
addMenuImage("seaweed", "YL4RcmB") # YL4RcmB
addMenuImage("chicken noodle soup", "jTeOF8R") # jTeOF8R
addMenuImage("fragrant snow", "x4MReA4") # x4MReA4
addMenuImage("Four-layered dip", "DD7vpz3") # DD7vpz3 ; green tea A4dfMST
addMenuImage("baked sweet potato", "3xnP7rV") # 3xnP7rV
addMenuImage("ocean", "Zdld97L") # Zdld97L


# populate conditions
populateConditions(data3["conditions"])
print "condition counts:", session.query(Condition).count()
myFirstCondition = session.query(Condition).filter_by(name="diabetes").first()

# create and link a special menu to a condition w/o committing menu first
if session.query(Condition).filter_by(name="constipation").first() is None:
    constipation = Condition(
        name="constipation",
        signs_and_symptoms="spending long time for bowel movement")
    kabocha = session.query(MenuItem).filter_by(name="baked kabocha squash").first()
    if kabocha is None:
        kabocha = MenuItem(
            name="baked kabocha squash",
            description="kabocha brushed with coconut oil roasted to a rich texture",
            price="$3.00",
            course="vegetable",
            restaurant=mySecondRestaurant)
        addMenuImage("baked kabocha squash",2)
    constipation.suggested_menus.append(kabocha)
    session.add(constipation)
    session.commit()

# verify the presence of kabocha menu
kabocha_menu = session.query(MenuItem).filter(MenuItem.name.like('%kabocha%')).first()
# print "kabocha?", kabocha_menu.description

# for album in client.get_account_albums('me'):
# album_title = album.title if album.title else 'Untitled'
# print('Album: {0} ({1})'.format(album_title, album.id))

# for image in client.get_album_images(album.id):
#     image_title = image.title if image.title else 'Untitled'
#     print('\t{0}: {1}'.format(image_title, image.link))
