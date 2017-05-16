#Project 3 of Udacity Full Stack Nanodegree: Therapeutic Foods
##Hosted
at http://ec2-34-208-105-239.us-west-2.compute.amazonaws.com/
##How to Run the Application

0. First install Python and Vagrant
1. At a directory, 'git clone {my project git url}',
2. cd to the project directory, run 'vagrant init ubuntu/trusty32'
3. At the project directory, run 'vagrant up', then 'vagrant ssh'
4. Inside vagrant: cd /vagrant/FoodsTherapy; at the master branch, run 'python
   finalProject.py'; follow the vm prompt to fetch the pin from imgur.com and enter it
   at the vm prompt; Further follow the direction of the vagrant VM and open the browser
   at address: localhost:5000.
5. To start with a clean database, do the following inside vagrant at /vagrant/Foods
   Therapy:
  - python database_setup.py
  - python manyRestaurants.py
  - python finalProject.py; follow the vm prompt to fetch the pin as in step 4 above.
6. When creating menuItem, upload the image from the project directory.

Features of My Application
1. A user will authenticate the app usage by either facebook or google+ authentication.
   The user will also fetch a pin from the imgur site after running finalProject.py to
   upload image at imgur and populate the image property of menuitem in the database.
2. A logged-in user can create, edit, and delete restaurants, the menus offered by his
   or her own restaurant, and a list of health conditions that couple with recommended
   menus.
3. A non-registered user can look through the restaurants, menu and conditions tabs without
   logging in. The user can find menus offered by a partiuclar restaurant, menus
   recommended for certain health conditions, and a list of all the menus created by all
   users.

Endpoints of My Application, APPLICATION_NAME = "Therapeutic Foods"

album_title = 'therapeutic menus' # album the user creates at imgur when uploading image

A decorator is a function that returns a function.
def login_required(f):
    """to wrap those methods that require login"""

def login_and_restauranter_required(f):
    """to wrap methods requiring login as the creator of the restaurant"""

def login_and_condition_required(f):
    """to wrap methods requiring login as the creator of the condition"""

@app.errorhandler(404)
def page_not_found(e):

@app.route('/login/')
def showLogin():
    """the page where users log in"""

@app.route('/gconnect/', methods=['POST'])
def gconnect():
    """authenticate via google +"""

@app.route('/gdisconnect/')
def gdisconnect():
    """disconnect from google +"""

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
