import os
import time
import calendar
import subprocess
from common.constants import tmp_scan_dir

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
		file_name = '%s.jpeg'%(ts)
		image_scanned = self._scan_image(file_name)
		image_cropped = self._crop_image(file_name, image_scanned)
		os.remove(image_scanned)
		image_final = os.path.join(self.path, file_name)
		self._set_datetime(date_created, image_cropped)
		os.rename(image_cropped, image_final)
		return image_final

	def batch_scan(self, date_created):
		ts = _get_timestamp()
		file_format = os.path.join(tmp_scan_dir, 'raw_'+str(ts)+'-%d.jpg')
		self._batch_scan(file_format)
		file_list = _get_files(tmp_scan_dir)
		for image_scanned in file_list:
			file_name = os.path.basename(image_scanned).replace("raw_", "")
			image_cropped = self._crop_image(file_name, image_scanned)
			os.remove(image_scanned)
			self._set_datetime(date_created, image_cropped)
			os.remove(image_cropped+'_original') # Created by exiftool
			image_final = os.path.join(self.path, file_name)
			os.rename(image_cropped, image_final)


	def _scan_image(self, file_name):
		raw_file_path = os.path.join(tmp_scan_dir, 'raw_%s'%(file_name))
		cmd = "scanimage --format=jpeg > %s" % (raw_file_path)
		subprocess.run(cmd, shell=True)
		return raw_file_path

	def _batch_scan(self, file_format):
		cmd = "scanimage --format=jpeg --batch=%s"%(file_format)
		subprocess.run(cmd, shell=True)

	def _crop_image(self, file_name, raw_file):
		processed_file_path = os.path.join(tmp_scan_dir, file_name)
		cmd = "convert %s -trim +repage %s" % (raw_file, processed_file_path)
		subprocess.run(cmd, shell=True)
		return processed_file_path

	def _set_datetime(self, date_created, file):
		cmd = 'exiftool "-DateTimeOriginal=%s:%s:%s 00:00:00" %s'\
			%(date_created.year, date_created.month, date_created.day, file)
		subprocess.run(cmd, shell=True)
