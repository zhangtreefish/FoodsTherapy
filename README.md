Project 3 of Udacity Full Stack Nanodegree: Therapeutic Foods

How to Run the Application

0. First install Python and Vagrant
1. At a directory, 'git clone {my project git url}',
2. cd to the project directory, run 'vagrant init ubuntu/trusty32'
3. At the project directory, run 'vagrant up', then 'vagrant ssh'
4. Inside vagrant: from th ecurrent (/home/vagrant) directory cd ..
twice to reach the root (/), then cd vagrant/FoodsTherapy, pwd to verify /vagrant/FoodsTherapy.
5. Inside vagrant at /vagrant/FoodsTherapy: Run in order 'python database_setup.py',
'python manyRestaurants.py', and 'python finalProject.py'; follow the vm prompt to fetch the pin from imgur.com and enter it at the vm prompt when running finalProject.py. An album titled 'therapeutic menus' is created by user at imgur when uploading images for menu
6. Further follow the direction of the vagrant VM and open the browser at address: localhost:5000

Features of My Application

1. A logged-in user can create, edit, and delete restaurants, menus offered by his or her own restaurant, and a list of health conditions that are associated with recommended menus. A logged-in user can also visit the restaurant serving a menu recommended for his or her conditions.
2. A non-registered user can look through all tabs (the restaurants,menu and conditions tabs) without logging in. The user can find menus offered by a partiuclar restaurant, menus recommended for certain health conditions, and a list of all the menus created by all users.
3. All users can also visit the restaurant serving a menu recommended for certain condition.

Endpoints of My Application, APPLICATION_NAME = "Therapeutic Foods"

album_title = 'therapeutic menus' # album the user creates at imgur when uploading image for menu

# A decorator is a function that returns a function.
def login_required(f):
    """to wrap those methods that require login"""

def login_and_restauranter_required(f):
    """to wrap methods requiring login as the creator of the restaurant"""

def login_and_condition_required(f):
    """to wrap methods requiring login as the creator of the condition"""

@app.route('/login/')
def showLogin():
    """the page where users log in"""

@app.route('/gconnect/', methods=['POST'])
def gconnect():
    """authenticate via google +"""

@app.route('/gdisconnect/')
def gdisconnect():
    """disconnect from google +"""

# TODO create user if have not yet
@app.route('/fbconnect/', methods=['POST'])
def fbconnect():
    """authenticate via FB"""

@app.route('/fbdisconnect/')
def fbdisconnect():

@app.route('/disconnect')
def disconnect():
    """provides a logout method for users"""

@app.route('/restaurants/JSON/')
def restaurantsJSON():
    """list of restaurants in JSON format"""

@app.route('/restaurants/xml/')
def restaurantsXml():
    """Return Xml format of restaurants list"""

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    """list of restaurants, varies upon user login status"""

@app.route('/restaurants/new/', methods=['POST', 'GET'])
@login_required
def restaurantNew():
    """let a logged-in user create a new restaurant"""

@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['POST', 'GET'])
@login_and_restauranter_required
def restaurantEdit(restaurant_id):
    """let a logged-in user edit his or her own restaurant"""

@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['POST', 'GET'])
@login_and_restauranter_required
def restaurantDelete(restaurant_id):
    """let a logged-in user delete his or her own restaurant"""

@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    """list of the menus of a particular restaurant in JSON format"""

@app.route('/menus/JSON/')
def allMenusJSON():
    """list of all the menus of all restaurants in JSON format"""

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuJSON(restaurant_id, menu_id):
    """list a particular menus of a particular restaurant in JSON format"""

@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenus(restaurant_id):
    """list of the menus of a restaurant, varies upon user login status"""

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
@login_and_restauranter_required
def newMenu(restaurant_id):
    """lets a restaurant owner create a new menu"""

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
@login_and_restauranter_required
def editMenu(restaurant_id, menu_id):
    """lets a restaurant owner edit a menu"""

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
@login_and_restauranter_required
def deleteMenu(restaurant_id, menu_id):
    """lets a restaurant owner delete a menu"""


@app.route('/conditions/')
def showConditions():
    """lists of health conditions, varies upon user login status"""

@app.route('/conditions/new/', methods=['POST', 'GET'])
@login_required
def newCondition():
    """lets a logged-in user create a new health condition for self"""

@app.route('/conditions/<int:condition_id>/edit', methods=['POST', 'GET'])
@login_and_condition_required
def conditionEdit(condition_id):
    """lets a user edit own health condition"""

@app.route('/conditions/<int:condition_id>/delete', methods=['POST', 'GET'])
@login_and_condition_required
def conditionDelete(condition_id):
    """lets a user delete own health condition"""

@app.route('/conditions/<int:condition_id>/menu/')
def conditionMenus(condition_id):
    """lists all menus suitable for a condition"""

@app.route('/conditions/<int:condition_id>/new/', methods=['GET', 'POST'])
@login_and_condition_required
def newConditionMenu(condition_id):
    """lets a user suggest a menu suitable for a condition"""
