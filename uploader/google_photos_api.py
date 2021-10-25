import requests
import os

def _gen_media_items(map_token_file):
	media_items = []
	for token in map_token_file.keys():
		file = map_token_file[token]
		file_name = os.path.basename(file)
		media_items.append({
			'simpleMediaItem': {
				'fileName': file_name,
				'uploadToken': token
			}
		})
	return media_items

""" Docs: https://developers.google.com/photos/library/guides/upload-media
"""
class GooglePhotosApi:
	def __init__(self, access_token):
		if access_token == None or access_token == '':
			raise Exception('Access Token is either null or empty')
		self.access_token = access_token

	"""
	Uploads images to Google Photos. This only uploads the data, and does not handle
	the actuall creation of the "media" object. 
	
	return: str - upload-token
	"""
	def upload_bytes(self, image_path):
		if not os.path.isfile(image_path) or os.path.getsize(image_path) == 0:
			raise ValueError('File %s either does not exist or is empty.'%(image_path))

		url = 'https://photoslibrary.googleapis.com/v1/uploads'
		fp = open(image_path, 'rb')
		data = fp.read()
		fp.close()
		headers = {
			'Authorization'				 : 'Bearer ' + self.access_token,
			'Content-type' 				 : 'application/octet-stream',
			'X-Goog-Upload-Content-Type' : 'image/jpeg',
			'X-Goog-Upload-Protocol' 	 : 'raw'
		}
		x = requests.post(url, headers=headers, data=data, timeout=60)

		if not x.ok:
			raise RuntimeError("Failed to upload file:%s"%(image_path), x.text)

		return x.text

	"""
	return: list - successfully uploaded tokens
	"""
	def batch_create(self, map_token_file):
		url = 'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate'
		json = { 'newMediaItems': _gen_media_items(map_token_file) }
		headers = {
			'Authorization' : 'Bearer ' + self.access_token,
			'Content-type' 	: 'application/json'
		}

		x = requests.post(url, headers=headers, json=json, timeout=60)
		if not x.ok:
			raise RuntimeError("Failed to create media items", x.text)

		successful_tokens = []
		response = x.json()
		results = response['newMediaItemResults']
		print(json)
		# print(response)
		for result in results:
			token = result['uploadToken']
			if "code" in result['status'].keys():
				print("Failed to upload %s -- Code %d: %s"%(map_token_file[token], result['status']['code'], result['status']['message']))
				continue
			successful_tokens.append(token)
		return successful_tokens