import os
from os.path import exists
_path = ".config"
_file = os.path.join(_path, 'access_token')

def save(token):
	os.makedirs(_path, exist_ok=True)
	try:
		f = open(_file, "w")
		f.write(token)
	finally:
		f.close()

def read():
	if not exists(_file):
		return ''
	os.makedirs(_path, exist_ok=True)
	try:
		f = open(_file, "r")
		token = f.read()
		return token
	finally:
		f.close()