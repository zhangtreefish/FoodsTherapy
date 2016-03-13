from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem, Condition, User, Base, engine
import json
import logging


# sessionmaker: a session factory generator (in other words, a function
# that returns a function that returns a new Session for each call)
DBSession = sessionmaker(bind=engine)
# Session: a container of instances of mapped classes
session = DBSession()

data = json.loads(open('app_data.json', 'r').read())
# print "resta!!!!!", data["restaurants"][0]


def populate(restaurant):
    """ populate a single restaurant, skip if already present"""
    if session.query(Restaurant).filter_by(name=restaurant["name"]).first() is None:
        restaurant = Restaurant(
            name=restaurant["name"],
            description=restaurant["description"])
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
                restaurant = Restaurant(
                    name=restaurants[i]["name"],
                    description=restaurants[i]["description"])
                session.add(restaurant)
            session.commit()
    except:
        return "Error: no restaurant is created."


# populate the restaurants
populateRestaurants(data["restaurants"])
restaurant_num = session.query(Restaurant).count()
# print 'number of restaurants populated:', restaurant_num

myFirstRestaurant = session.query(Restaurant).filter_by(name="Steam").first()
mySecondRestaurant = session.query(Restaurant).filter_by(name="3Fs").first()
myThirdRestaurant = session.query(Restaurant).filter_by(name="Eden").first()
myFourthRestaurant = session.query(Restaurant).filter_by(name="School Lunch").first()
# print "second?:", mySecondRestaurant


def populateMenus(menus,restaurant):
    """ method to populate a list of menus, skip if already present"""
    try:
        for i in range(len(menus)):
            if session.query(MenuItem).filter_by(name=menus[i]["name"]).first() is None:
                menu = MenuItem(name=menus[i]["name"],
                                description=menus[i]["description"],
                                price=menus[i]["price"],
                                course=menus[i]["course"],
                                image=menus[i]["image"],
                                restaurant=restaurant)
                session.add(menu)
            session.commit()
    except:
        return "Error: no menu is created."


# populate the menus
populateMenus([data['menus'][0], data['menus'][1]], myFirstRestaurant)
populateMenus([data['menus'][4], data['menus'][6], data['menus'][7]], mySecondRestaurant)
populateMenus(data['menus'][2], myThirdRestaurant)
populateMenus([data['menus'][3], data['menus'][5], data['menus'][8]], myFourthRestaurant)
menu_no = session.query(MenuItem).count()
print 'menu number:', menu_no


def populateConditions(conditions):
    """ method to populate a list of conditions, skip if already present"""
    try:
        for i in range(len(conditions)):
            if session.query(Condition).filter_by(name=conditions[i]["name"]).first() is None:
                condition = Condition(name=conditions[i]["name"],
                                      signs_and_symptoms=conditions[i]["signs_and_symptoms"])
                session.add(condition)
            session.commit()
    except:
        return "Error: no condition is created."


# populate conditions
populateConditions(data["conditions"])
con_count = session.query(Condition).count()
print "condition counts:", con_count
# myFirstCondition = session.query(Condition).filter_by(name="diabetes").first()


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
            image="http://i.imgur.com/71kZSj7.jpg", #can set the image here
            restaurant=mySecondRestaurant)
    constipation.suggested_menus.append(kabocha)
    session.add(constipation)
    session.commit()


# for album in client.get_account_albums('me'):
# album_title = album.title if album.title else 'Untitled'
# print('Album: {0} ({1})'.format(album_title, album.id))

# for image in client.get_album_images(album.id):
#     image_title = image.title if image.title else 'Untitled'
#     print('\t{0}: {1}'.format(image_title, image.link))
