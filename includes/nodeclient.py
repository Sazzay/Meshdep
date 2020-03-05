import socket
import os
import platform
import subprocess

class NodeClient:
	def __init__(self, ip, port):
		self.ACTIVE = False
		self.IP = ip
		self.PORT = int(port)
		self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		test = self.fetch_mid()
		print(test)

		self.add_file("Svantesson", "Min skit", "porr.mp4", b'10101')
		self.rm_file("Svantesson", "Min skit", "porr.mp4")

		try:
			self.ACTIVE = True
			self.SOCK.connect((self.IP, self.PORT))

			print("[NODE] Successfully established a connection to %s:%s" % (self.IP, self.PORT))
		except:
			print("[NODE] Failed to establish a connection to %s:%s" % (self.IP, self.PORT))

	def __repr__(self):
		return "%s:%s" % (self.IP, self.PORT)

	def fetch_mid(self):
		if platform.system() == "Linux":
			try:
				return os.popen("cat /etc/machine-id").read()
			except:
				print("[NODE] There was an error trying to fetch /etc/machine-id.")

		if platform.system() == "Windows":
			try:
				return subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
			except:
				print("[NODE] Subprocess WMIC failed to fetch /etc/machine-id UUID equilivent.")

	def add_file(self, user, path, file_name, data):
		if os.path.exists('Data' + '/' + user + '/' + path):
			f = open('Data' + '/' + user + '/' + path + '/' + file_name, "wb")
			f.write(data)
			f.close()
		else:
			self.add_folder(user, path)
			self.add_file(user, path, file_name, data)

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