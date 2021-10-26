import os
import json
from os.path import exists
_path = ".config"
_file = os.path.join(_path, 'access_token')

def save(token, expired_time):
	os.makedirs(_path, exist_ok=True)
	data = json.dumps({
		'token': token,
		'expired_time': expired_time 
	})
	try:
		f = open(_file, "w")
		f.write(data)
	finally:
		f.close()

def _read():
	if not exists(_file):
		return ''
	os.makedirs(_path, exist_ok=True)
	try:
		f = open(_file, "r")
		data = f.read()
		return data
	finally:
		f.close()

def get_token():
	text = _read()
	if text == '':
		return text
	data = json.loads(text)
	return data['token']

def get_expired_time():
	text = _read()
	if text == '':
		return None
	data = json.loads(text)
	return data['expired_time']

def clear():
	try:
		f = open(_file, "w")
		f.write('')
	finally:
		f.close()
