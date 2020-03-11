import os

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
		except Exception as ex:
			print("[NODE] FileAdder failed to open a new file at %s with filename %s with exception %s" % (self.PATH, self.FILENAME, ex))

	def __repr__(self):
		return 'Data' + '/' + self.USER + '/' + self.PATH + '/' + self.FILENAME

	def write(self, data):
		self.FILEOBJ.write(data)

	def close(self):
		self.FILEOBJ.close()


def rm_file(self, user, path, file_name):
	if os.path.isfile('Data' + '/' + user + '/' + path + '/' + file_name):
		os.remove('Data' + '/' + user + '/' + path + '/' + file_name)
	else:
		print("[NODE] The path specified is not a file, can not complete.")

def add_folder(self, user, path):
	if not os.path.exists('Data' + '/' + user + '/' + path):
		os.makedirs('Data' + '/' + user + '/' + path)
	else:
		print("[NODE] Tried to add a folder that already exist.")

def rm_folder(self, user, path):
	if os.path.exists('Data' + '/' + user + '/' + path):
		os.removedirs('Data' + '/' + user + '/' + path)
	else:
		print("[NODE] Tried to remove a folder that does not exist.")