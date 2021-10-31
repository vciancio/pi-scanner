import os
from decouple import config

class Config:
	GOOGLE_PHOTOS_CLIENT_SECRET = config('GOOGLE_PHOTOS_CLIENT_SECRET')
	GOOGLE_PHOTOS_CLIENT_ID = config('GOOGLE_PHOTOS_CLIENT_ID')
	DIR_SCANNED_PHOTOS = config('DIR_SCANNED_PHOTOS', default='/home/pi/scanned_photos')
	PHOTO_FORMAT = config('PHOTO_FORMAT', default='png')