import os
import time
import calendar
import subprocess
from datetime import datetime
from common.constants import tmp_scan_dir
from common.config import Config
from PIL import Image, ImageChops

_TRIM_ITERATIONS = 2
_TRIM_FUZZ = 20
_FORMAT = Config.PHOTO_FORMAT

def _get_files(folder):
	file_list = []
	for name in os.listdir(folder):
		file = os.path.join(folder, name)
		if os.path.isfile(file):
			file_list.append(file)
	return file_list

def _get_timestamp():
	gmt = time.gmtime()
	return calendar.timegm(gmt)

class Scanner():
	def __init__(self, path):
		self.path = path
		os.makedirs(path, exist_ok=True)
		os.makedirs(tmp_scan_dir, exist_ok=True)

	def scan_image(self, date_created):
		ts = _get_timestamp()
		file_name = '%s.%s'%(ts, _FORMAT)
		image_scanned = self._scan_image(file_name)
		image_cropped = self._crop_image(file_name, image_scanned)
		os.remove(image_scanned)
		image_final = os.path.join(self.path, file_name)
		self._set_datetime(date_created, image_cropped)
		os.rename(image_cropped, image_final)
		return image_final

	def batch_scan(self, date_created):
		ts = _get_timestamp()
		file_name_base = 'SCAN_%s%02d%02d_000000-%d'%(date_created.year, date_created.month, date_created.day, ts)
		file_format = os.path.join(tmp_scan_dir, 'raw_'+file_name_base+'-%d.'+_FORMAT)
		self._batch_scan(file_format)

		file_list = _get_files(tmp_scan_dir)
		for image_scanned in file_list:
			file_name = os.path.basename(image_scanned).replace("raw_", "")
			
			# Photo Manipulation
			self._crop_image(image_scanned)
			
			# Exif Modification
			self._set_datetime(date_created, image_scanned)
			try:
				os.remove(image_scanned+'_original') # Created by exiftool
			except:
				pass
			
			# Output
			image_final = os.path.join(self.path, file_name)
			os.rename(image_scanned, image_final)

	def _scan_image(self, file_name):
		raw_file_path = os.path.join(tmp_scan_dir, 'raw_%s'%(file_name))
		cmd = "scanimage --format=%s > %s" % (_FORMAT, raw_file_path)
		subprocess.run(cmd, shell=True)
		return raw_file_path

	def _batch_scan(self, file_format):
		cmd = "scanimage --format=%s --batch=%s"%(_FORMAT, file_format)
		subprocess.run(cmd, shell=True)

	def _crop_image(self, file):
		cmd = "convert " + file + " -quality 100 -fuzz " + str(_TRIM_FUZZ) + "% -trim +repage " + file
		for i in range(_TRIM_ITERATIONS):
			subprocess.run(cmd, shell=True)

	def _resize(self, file):
		cmd = "convert " + file + " -quality 100 -resize x750 -unsharp 0x1 " + file
		subprocess.run(cmd, shell=True)

	def _trim(self, old_file, new_file):
		im = Image.open(old_file)
		bg = Image.new(im.mode, im.size, im.getpixel((10,10)))
		diff = ImageChops.difference(im, bg)
		diff = ImageChops.add(diff, diff)
		#Bounding box given as a 4-tuple defining the left, upper, right, and lower pixel coordinates.
		#If the image is completely empty, this method returns None.
		bbox = diff.getbbox()
		print(bbox)
		if bbox:
		    im = im.crop(bbox)
		im.save(new_file)

	def _set_datetime(self, date_created, file):

		if _FORMAT == 'png':
			args = ' '.join([
				'"-PNG:CreationTime=%s:%s:%s 00:00:00"'%(date_created.year, date_created.month, date_created.day),
				'"-EXIF:DateTimeOriginal=%s:%s:%s 00:00:00"'%(date_created.year, date_created.month, date_created.day),
				'"-DateTimeOriginal=%s:%s:%s 00:00:00"'%(date_created.year, date_created.month, date_created.day),
				'"-PNG:CreateDate=%s:%s:%s 00:00:00"'%(date_created.year, date_created.month, date_created.day),
			])
		elif _FORMAT == 'jpeg':
			args = ' '.join([
				'"-DateTimeOriginal=%s:%s:%s 00:00:00"'%(date_created.year, date_created.month, date_created.day),
			])
		elif _FORMAT == 'tiff':
			now = datetime.now()
			args = ' '.join([
				'"-DateTimeOriginal=%s:%s:%s 00:00:00"'%(date_created.year, date_created.month, date_created.day),
				'"-CreateDate=%s:%s:%s %s:%s:%s"'%(now.year, now.month, now.day, now.hour, now.minute, now.second)
			])
		else:
			args =  ''
		
		if len(args) > 0:
			cmd = ' '.join([
				'exiftool',
				args,
				file
			])
			subprocess.run(cmd, shell=True)

		cmd = ' '.join([
			'touch',
			'-t %s%s010000.11'%(date_created.year, date_created.month),
			file
		])
		subprocess.run(cmd, shell=True)
