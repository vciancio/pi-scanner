import os
import time
import subprocess

dir_tmp_img = './tmp_img'

def _get_timestamp():
	import calendar
	import time
	gmt = time.gmtime()
	return calendar.timegm(gmt)

class Scanner():
	def __init__(self, path):
		self.path = path

	def scan_image(self, date_created):
		ts = _get_timestamp()
		file_name = '%s.jpeg'%(ts)
		image_scanned = self._scan_image(file_name)
		image_cropped = self._crop_image(file_name, image_scanned)
		os.remove(image_scanned)
		image_final = os.path.join(self.path, file_name)
		self._set_datetime(date_created, image_cropped)
		os.rename(image_cropped, image_final)
		return image_final

	def _scan_image(self, file_name):
		raw_file_path = os.path.join(dir_tmp_img, 'raw_%s'%(file_name))
		cmd = "scanimage --format=jpeg > %s" % (raw_file_path)
		subprocess.run(cmd, shell=True)
		return raw_file_path

	def _crop_image(self, file_name, raw_file):
		processed_file_path = os.path.join(dir_tmp_img, file_name)
		cmd = "convert %s -trim +repage %s" % (raw_file, processed_file_path)
		subprocess.run(cmd, shell=True)
		return processed_file_path

	def _set_datetime(self, date_created, file_name):
		cmd = 'exiftool "-DateTimeOriginal=%s:1:1 00:00:00" %s'%(date_created.year, file_name)
		subprocess.run(cmd, shell=True)
