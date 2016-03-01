Project 3 of Udacity Full Stack Nanodegree: Therapeutic Foods

How to Run the Application

0. First install Python and Vagrant
1. At a directory, 'git clone {my project git url}',
2. cd to the project directory, run 'vagrant init ubuntu/trusty32'
3. At the project directory, run 'vagrant up', then 'vagrant ssh'
4. inside vagrant: cd .. twice, then cd vagrant/FoodsTherapy, pwd to verify ~/vagrant/FoodsTherapy.
Run 'python database_setup.py', 'python manyRestaurants.py', and 'python finalProject.py'
5. Follow the direction of the vagrant VM and open the browser at address: localhost:5000

Features of My Application
1. A logged-in user can create, edit, and delete restaurants, menus offered by his or her own restaurant, and a list of health conditions that are associated with recommended menus. A logged-in user can also visit the restaurant serving a menu recommended for his or her conditions.
2. A non-registered user can look through all tabs (the restaurants,menu and conditions tabs) without logging in. The user can find menus offered by a partiuclar restaurant, menus recommended for certain health conditions, and a list of all the menus created by all users.
3. All users can also visit the restaurant serving a menu recommended for certain condition.
