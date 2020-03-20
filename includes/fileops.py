from includes import utils
import os
import shutil

class FileAdder:
	def __init__(self, user, filename, path):
		self.FILEOBJ = None
		self.USER = user
		self.FILENAME = filename
		self.PATH = path

		try:
			originalName = self.FILENAME
			count = 0

			while os.path.isfile('Data' + '/' + self.USER + '/' + self.PATH + '/' + self.FILENAME):
				count += 1
				split = os.path.splitext(originalName)
				self.FILENAME = split[0] + '_' + str(count) + split[1]

			if not os.path.exists('Data' + '/' + user + '/' + path):
				os.makedirs('Data' + '/' + user + '/' + path)
			
			self.FILEOBJ = open('Data' + '/' + self.USER + '/' + self.PATH + '/' + self.FILENAME, "wb")
			utils.log("[NODE] FileAdder added a new file with filename %s" % self.FILENAME, True)
		except Exception as ex:
			utils.log("[NODE] FileAdder failed to open a new file at %s with filename %s with exception %s" % (self.PATH, self.FILENAME, ex), True)

	def __repr__(self):
		return 'Data' + '/' + self.USER + '/' + self.PATH + '/' + self.FILENAME

	def write(self, data):
		self.FILEOBJ.write(data)

	def close(self):
		self.FILEOBJ.close()


def rm_file(user, path, filename):
	if os.path.isfile('Data' + '/' + user + '/' + path + '/' + filename):
		os.remove('Data' + '/' + user + '/' + path + '/' + filename)
	else:
		utils.log("[NODE] The path specified is not a file, can not complete.", True)
		raise FileNotFoundError

def add_folder(user, path):
	if not os.path.exists('Data' + '/' + user + '/' + path):
		os.makedirs('Data' + '/' + user + '/' + path)
	else:
		utils.log("[NODE] User %s tried to add a folder that already exist." % user, True)
		raise FileExistsError

def rm_folder(user, path):
	if os.path.exists('Data' + '/' + user + '/' + path):
		try:
			shutil.rmtree('Data' + '/' + user + '/' + path)
		except Exception as ex:
			utils.log("[NODE] User %s got exception %s while trying to remove folder" % (user, ex), True)
	else:
		utils.log("[NODE] User %s tried to remove a folder that does not exist." % user, True)
		raise FileNotFoundError