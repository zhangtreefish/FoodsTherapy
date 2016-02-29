#!/usr/bin/env python3

'''
	Here's how you upload an image. For this example, put the cutest picture
	of a kitten you can find in this script's folder and name it 'Kitten.jpg'

	For more details about images and the API see here:
		https://api.imgur.com/endpoints/image
'''

# Pull authentication from the auth example (see auth.py)
from auth import authenticate
from datetime import datetime


image_path_default = 'daikon.jpg'


def upload_image(client, image_name, image_path=image_path_default):
	'''
	Upload a picture of the menu item to the app author's
	Menu Image album at imgur.com
	'''
	# client = authenticate()
	# get my first album's id
	ids = client.get_account_album_ids('Zhangtreefish')
	album_id = ids[0]

	# Here's the metadata for the upload. All of these are optional, including
	# this config dict itself.
	config = {
		'album': album_id,
		'name':  image_name,
		'title': '',
		'description': ' on date {0}'.format(datetime.now())
	}

	print("Uploading image... ")
	image = client.upload_from_path(image_path, config=config, anon=False)
	print("Done")
	print()
	print('image', image)
	return image


# If you want to run this as a standalone script
if __name__ == "__main__":
	client = authenticate()
	image = upload_image(client, 'daikon', image_path_default)

	print("Image was posted! Go check your images!")
	print("You can find it here: {0}".format(image['link']))