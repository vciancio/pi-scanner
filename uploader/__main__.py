import os
import requests
import time
from uploader.google_photos_api import GooglePhotosApi
from common.config import Config
import common.access_token as access_token
import sys

def get_photos_to_upload():
	photo_list = []
	for name in os.listdir(Config.DIR_SCANNED_PHOTOS):
		path = '%s/%s'%(Config.DIR_SCANNED_PHOTOS,name)
		if not os.path.isfile(path):
			continue
		photo_list.append(path)
	return photo_list


## returns map(photo_path : upload_token)
def upload_photos(api, photo_list):
	uploaded_map = {}
	for photo_path in photo_list:
		try:
			upload_token = api.upload_bytes(photo_path)
		except (RuntimeError, ValueError):
			print('Failed to upload file: ', photo_path)
			continue

		uploaded_map[upload_token] = photo_path
	return uploaded_map

if __name__ == '__main__':
	token = access_token.read()

	# Check if we even have an access token
	if token is None or token == '':
		sys.exit(1)

	api = GooglePhotosApi(token)
	photo_list = get_photos_to_upload()[:50]
	if len(photo_list) < 1:
		print("No photos to upload")
		sys.exit(1)

	print("Uploading Photo Binaries")
	map_token_file = upload_photos(api, photo_list)
	if len(map_token_file.keys()) < 1:
		print("No uploaded photo binaries")
		sys.exit(1)

	print("Performing Batch Create API Call")
	uploaded_tokens = api.batch_create(map_token_file)
	for upload_token in uploaded_tokens:
		print('deleting ', map_token_file[upload_token])
		os.remove(map_token_file[upload_token])
