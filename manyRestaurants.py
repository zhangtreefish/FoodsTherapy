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

data = {
    "restaurants": [
        {"name":"Steam", "description":"all things steamed"},
        {"name":'3Fs', "description":'that features fiber,fitness, and fluid'},
        {"name":'Eden', "description":'out of your dream garden'},
        {"name":'School Lunch',
        "description":"balanced lunch for the precious bodies and minds"}
    ]
}

# populate a single restaurant
def populate(restaurant):
    restaurant = Restaurant(name=restaurant["name"], description=restaurant["description"])
    session.add(restaurant)
    session.commit()


# populate a list of restaurants
def populateRestaurant(restaurants):
    try:
        for i in range(len(restaurants)):
            restaurant = Restaurant(name=restaurants[i]["name"], description=restaurants[i]["description"])
            session.add(restaurant)
        session.commit()
    except:
        return "Error: no restaurant is created."


populateRestaurant(data["restaurants"])

restaurant_num = session.query(Restaurant).count()
print 'number of restaurants populated:', restaurant_num

myFirstRestaurant = session.query(Restaurant).first()
mySecondRestaurant = session.query(Restaurant).filter_by(id=2).one()
myThirdRestaurant = session.query(Restaurant).filter_by(id=3).one()
myFourthRestaurant = session.query(Restaurant).filter_by(id=4).one()
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
         "restaurant": mySecondRestaurant},
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
        myFourthRestaurant}
    ]
}

# populate a list of menus
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

populateMenu(data2['menus'])

# myFirstMenu = MenuItem(
#     name='jade',
#     description='daikon steamed to a luscious texture',
#     price='$2.50',
#     course='vegetable',
#     restaurant=myFirstRestaurant)
# mySecondMenu = MenuItem(name='fragrant snow',
#                         description='sweet rice flour balls encasing \
#                         honey-infused sweet olive blossoms and coconut oil',
#                         price='$4.00',
#                         course='dessert',
#                         restaurant=myFirstRestaurant)
# myThirdMenu = MenuItem(name='Four-layered dip',
#                        description='organic black beans, avacado, tomato, \
#                        cheese, dressed in lemon juice, served with tortilla\
#                         chips',
#                        price='$4.00',
#                        course='One Complete Meal',
#                        restaurant=mySecondRestaurant)
# myFourthMenu = MenuItem(name='chicken noodle soup',
#                         description='what else can you say? made with carrots,\
#                         celery, onion,garlic, tomato, zucchini, and ginger \
#                         root',
#                         price='$5.00',
#                         course='One Complete Meal',
#                         restaurant=myFourthRestaurant)
# myFifthMenu = MenuItem(name='ocean',
#                        description='soup made of tilapia,  celery, cilantro,\
#                         green onion,garlic, tomato, zucchini, and ginger root',
#                        price='$5.00',
#                        course='One Complete Meal',
#                        restaurant=myFourthRestaurant)
# mySixthMenu = MenuItem(name='seaweed',
#                        description='Wakame salad in green onion, hemp heart,\
#                        sesame oil, and salt,served with two pieces of baked \
#                        tofu, and a baked sweet potato',
#                        price='$5.00',
#                        course='One Complete Meal',
#                        restaurant=mySecondRestaurant)
# mySeventhMenu = MenuItem(name='ocean',
#                          description='soup made of tilapia,  celery, cilantro,\
#                          green onion,garlic, tomato, zucchini, and ginger \
#                          root',
#                          price='$5.00',
#                          course='One Complete Meal',
#                          restaurant=myFourthRestaurant)
# session.add(myFirstMenu)
# session.add(mySecondMenu)
# session.add(myThirdMenu, myFourthMenu)
# # session.add(myFourthMenu)
# session.add(myFifthMenu)
# session.add(mySixthMenu)
# session.add(mySeventhMenu)
# session.commit()
menu_no = session.query(MenuItem).count()
print 'menu number:', menu_no  # works

myFirstCondition = Condition(name='diabetes',
                             signs_and_symptoms='thirst, fatigue,\
                              frequent urination, weight loss')
mySecondCondition = Condition(name='gray hair',
                              signs_and_symptoms='natural graying of hair')
session.add(mySecondCondition)
session.commit()
# link a menu to myFirstCondition
diabeticMenu1 = MenuItem(name='baked sweet potato',
                         description='sweet potato baked at 350 for 45 minutes,\
                          with skin',
                         price='$3.00',
                         course='vegetable',
                         restaurant=myFirstRestaurant)
# session.add(diabeticMenu1)
# session.commit()
myFirstCondition.suggested_menus.append(diabeticMenu1)
session.add(myFirstCondition)
session.commit()
firstCon = session.query(Condition).first()
print firstCon.name
# print firstCon.suggested_menus.count()
# TODO above: why diabeticMenu1 not in the list?
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

myFirstUser = User(name='treefish', email='zhangtreefish@yahoo.com',
                   picture='')
mySecondUser = User(name='bob', email='fearlessluke8@gmail.com',
                    picture='http://i.imgur.com/3L3kK3q.png?1')

session.add(mySecondUser)
session.commit()
# The following unnecessary: the associations were already present,
# see project.py newMenu()
# myFirstUser.restaurants.append(myFirstRestaurant)
# myFirstUser.conditions.append(myFirstCondition)
# myFirstUser.menus.append(myFirstMenu)
# myFirstUser.menus.append(mySecondMenu)
session.add(myFirstUser)
session.commit()
