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
album_id=None

# TODO: album is created, but id is None
def create_album(album_title):
    """create an album for registered user in imgur.com"""
    album_config = {
    'title': album_title,
    'description': 'images of menus {0}'.format(datetime.now())
    }
    # client = authenticate()
    # check if titled album already exist
    client = authenticate()
    albums = client.get_account_albums('me')
    print "albums:", albums
    no_album = True
    album_id = None
    for a in albums:
        print "album", a.id, a.title
        if a.title == album_title:
            album_id = a.id
            no_album = False
            print ("album already exist, id is %s" % album_id)
            return album_id # need to return id!!
    # print "album1", album #works
    if no_album:
        album=client.create_album(album_config)
        after_albums = client.get_account_albums('me')
        for a in after_albums:
            if a.title == album_title:
                album_id = a.id
                return album_id


def create_album_simple(album_title):
    """
    create an album for registered user in imgur.com,
    return value is album id
    """
    album_config = {
    'title': album_title,
    'description': 'images of menus {0}'.format(datetime.now())
    }
    # client = authenticate()
    # check if titled album already exist
    client = authenticate()
    client.create_album(album_config)
    albums = client.get_account_albums('me')
    for a in albums:
        if a.title == album_title:
            album_id = a.id
            return album_id


# If you want to run this as a standalone script
if __name__ == "__main__":
	# the client can be made either here or inside method create_album_simple
	# client = authenticate()
	# if create album and then delete it, can not create another by the same title
	if album_id is None:
		album_id = create_album_simple('test2 album')

		print ("album with id %s created. Go check your album!" % album_id)
	print ("album with id %s exists. Go check your album!" % album_id)
	# print("You can find it here: {0}".format(album['link']))