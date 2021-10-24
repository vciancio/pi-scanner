from PIL import ImageFont

_size_xsmall = 8
_size_small = 10
_size_medium = 12
_size_large = 14

_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def xsmall():
	return (ImageFont.truetype(_path, _size_xsmall), _size_xsmall)

def small():
	return (ImageFont.truetype(_path, _size_small), _size_small)

def medium():
	return (ImageFont.truetype(_path, _size_medium), _size_medium)

def large():
	return (ImageFont.truetype(_path, _size_large), _size_large)