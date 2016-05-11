# Therapeutic Foods

hosted at http://ec2-52-38-199-253.us-west-2.compute.amazonaws.com/

0. First install Python and Vagrant
1. At a directory, 'git clone {my project git url}',
2. cd to the project directory, run 'vagrant init ubuntu/trusty32'
3. At the project directory, run 'vagrant up', then 'vagrant ssh'
4. Inside vagrant: from the current (/home/vagrant) directory cd ..
twice to reach the root (/), then cd vagrant/FoodsTherapy, pwd to verify /vagrant/FoodsTherapy.
5. Inside vagrant at /vagrant/FoodsTherapy: Run in order 'python database_setup.py',
'python manyRestaurants.py', and 'python finalProject.py'; follow the vm prompt to fetch the pin from imgur.com and enter it at the vm prompt when running finalProject.py. Upload an image when creating menuItem from the project directory, and an album titled 'therapeutic menus' containing the image will be created at imgur.
6. Further follow the direction of the vagrant VM and open the browser at address: localhost:5000

# Features of My Application
-- A logged-in user can
  -- create, edit, and delete restaurants,
  -- create, edit, and delete menus offered by his or her own restaurant,
  -- create, edit, and deleted a list of health conditions that are associated with recommended menus.
-- A non-registered user can look through all tabs without logging in through facebook or google plus.
-- The app aims to encourage users to eat towards health.

# Prospects for Collaboration
-- All users are encouraged to recommend favorite restaurants to be linked to this app.

