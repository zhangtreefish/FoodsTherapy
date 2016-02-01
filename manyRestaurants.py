from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem, Condition, User, Base, engine
import json
import logging

# from imgurpython import ImgurClient # TODO:no module


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
print 'number of restaurants populated:', restaurant_num

myFirstRestaurant = session.query(Restaurant).filter_by(name="Steam").first()
mySecondRestaurant = session.query(Restaurant).filter_by(name="3Fs").first()
myThirdRestaurant = session.query(Restaurant).filter_by(name="Eden").first()
myFourthRestaurant = session.query(Restaurant).filter_by(name="School Lunch").first()
print "second:", mySecondRestaurant

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
        "vegetable", "restaurant": mySecondRestaurant}
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
print 'menu number:', menu_no


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


# populate conditions
populateConditions(data3["conditions"])
print "condition counts:", session.query(Condition).count()
myFirstCondition = session.query(Condition).filter_by(name="diabetes").first()

# create and link a special menu to a condition w/o committing menu first
constipation = Condition(name="constipation",signs_and_symptoms="spending \
                         long time for bowel movement")
kabocha = MenuItem(
    name="baked kabocha squash",
    description="kabocha brushed with coconut oil roasted to a rich texture",
    price="$3.00",
    course="vegetable",
    restaurant=mySecondRestaurant)
constipation.suggested_menus.append(kabocha)
session.add(constipation)
session.commit()
kabocha_menu = session.query(MenuItem).filter(MenuItem.name.like('%kabocha%')).first()
print "kabocha?", kabocha_menu.description


# to get image from imgur:
# client_id = '32dba864f458125'
# client_secret = 'YOUR CLIENT SECRET'
# client = ImgurClient(client_id,client_secret)
# img1='client.getAlbumImages(0)'
# img2='https://api.imgur.com/3/image/{id}'

# Example request
# items = client.gallery()
# for item in items:
#     print "pic-link:",item.link

# myFirstUser = User(name='treefish', email='zhangtreefish@yahoo.com',
#                    picture='')
# mySecondUser = User(name='bob', email='fearlessluke8@gmail.com',
#                     picture='http://i.imgur.com/3L3kK3q.png?1')

