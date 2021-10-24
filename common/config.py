import os
from decouple import config

class Config:
	GOOGLE_PHOTOS_CLIENT_SECRET = config('GOOGLE_PHOTOS_CLIENT_SECRET')
	GOOGLE_PHOTOS_CLIENT_ID = config('GOOGLE_PHOTOS_CLIENT_ID')