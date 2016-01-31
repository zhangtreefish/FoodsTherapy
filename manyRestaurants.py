from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem, Condition, User, Base
import json

# from imgurpython import ImgurClient # TODO:no module

engine = create_engine('sqlite:///restaurantmenuconditionuser.db', echo=True)
# Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
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
    if session.query(Restaurant).filter_by(name=restaurant["name"]) is None:
        restaurant = Restaurant(name=restaurant["name"], description=restaurant["description"])
        session.add(restaurant)
        session.commit()
    else:
        return "Restaurant"+ restaurant + " already present."


def populateRestaurants(restaurants):
    """ to populate a list of restaurants, skip if already present"""
    try:
        for i in range(len(restaurants)):
            rest = session.query(Restaurant).filter_by(name=restaurants[i]["name"]).one()
            if rest is None:
                restaurant = Restaurant(name=restaurants[i]["name"], description=restaurants[i]["description"])
                session.add(restaurant)
            else:
                i += 1
            session.commit()
    except:
        return "Error: no restaurant is created."


def populateRestaurant(restaurants):
    """ to populate a list of restaurants, without checking"""
    try:
        for i in range(len(restaurants)):
            restaurant = Restaurant(name=restaurants[i]["name"], description=restaurants[i]["description"])
            session.add(restaurant)
            session.commit()
    except:
        return "Error: no restaurant is created."


# populate the restaurants
populateRestaurant(data1["restaurants"])
restaurant_num = session.query(Restaurant).count()
print 'number of restaurants populated:', restaurant_num

myFirstRestaurant = session.query(Restaurant).filter_by(name="Steam").first()
mySecondRestaurant = session.query(Restaurant).filter_by(name="3Fs").first()
myThirdRestaurant = session.query(Restaurant).filter_by(name="Eden").first()
myFourthRestaurant = session.query(Restaurant).filter_by(name="School Lunch").first()
print "second:",mySecondRestaurant.name

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
        {"name":"ocean","description":"soup made of tilapia,  celery, \
        cilantro, green onion,garlic, tomato, zucchini, and ginger root",
         "price": "$5.00", "course": "One Complete Meal", "restaurant"
         :myFourthRestaurant},
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
            if session.query(MenuItem).filter_by(name=menus[i]["name"]).one() is None:
                menu = MenuItem(name=menus[i]["name"],
                                description=menus[i]["description"],
                                price=menus[i]["price"],
                                course=menus[i]["course"],
                                restaurant=menus[i]["restaurant"])
                session.add(menu)
            else:
                i += 1
        session.commit()
    except:
        return "Error: no menu is created."

def populateMenu(menus):
    try:
        for i in range(len(menus)):

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
populateMenu(data2['menus'])
menu_no = session.query(MenuItem).count()
print 'menu number:', menu_no  # works


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
            if session.query(Condition).filter(name=conditions[i]["name"]).one() is None:
                condition = Condition(name=conditions[i]["name"],
                                      signs_and_symptoms=conditions[i]["signs_and_symptoms"])
                session.add(condition)
            else:
                i += 1
            session.commit()
    except:
        return "Error: no condition is created."


def populateCondition(conditions):
    try:
        for i in range(len(conditions)):
            condition = Condition(name=conditions[i]["name"],
                                  signs_and_symptoms=conditions[i]["signs_and_symptoms"])
            session.add(condition)

        session.commit()
    except:
        return "Error: no condition is created."

# populate conditions
populateCondition(data3["conditions"])
myFirstCondition = session.query(Condition).filter_by(name="diabetes").one()
print "condiiton:", myFirstCondition

# link a special menu to myFirstCondition
sweetPotatoMenu = session.query(MenuItem).filter(MenuItem.name.like('%sweet potato%')).first()
print "sweet potato?:" , sweetPotatoMenu.name

# session.add(diabeticMenu1)
# session.commit()

myFirstCondition.suggested_menus.append(sweetPotatoMenu)
session.add(myFirstCondition)
session.commit()

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

