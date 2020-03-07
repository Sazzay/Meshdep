import socket
import os
import platform
import subprocess
import psutil
from includes import packets

class NodeClient:
	def __init__(self, ip, port):
		self.TRANSFERS = []
		self.ACTIVE = False
		self.IP = ip
		self.PORT = int(port)
		self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			self.ACTIVE = True
			self.SOCK.connect((self.IP, self.PORT))

			print("[NODE] Successfully established a connection to %s:%s" % (self.IP, self.PORT))
		except:
			print("[NODE] Failed to establish a connection to %s:%s" % (self.IP, self.PORT))

		self.send_handshake()

	def __repr__(self):
		return "%s:%s" % (self.IP, self.PORT)

	# send functions #
	def send_handshake(self):
		mid = self.fetch_mid()
		self.SOCK.send((
			packets.fetchSmallPacket(
			packets.Packets.HANDSHAKE, 
			mid).encode()
			))

	def send_space_resp(self):
		space = self.fetch_avail_space()

		self.SOCK.send((
			packets.fetchSmallPacket(
			packets.Packets.RESP_SPACE, 
			space).encode()
			))

		print("[NODE] Received a space request, sending space response: %s" % space)

	def send_transfer_resp(self, port):
		# fetch an availble port based on
		# active socket threads in 

		self.SOCK.send((
			packets.fetchSmallPacket(
			packets.Packets.RESP_TRANSFER, 
			port).encode()
			))
	# recv functions #

	# cleanse functions #
	def cleanse_transfers(self):
		transfers = []

		for i in range(len(self.TRANSFERS)):
			if self.TRANSFERS[i].isAlive():
				transfers.append(self.TRANSFERS[i])

		self.TRANSFERS = transfers

	# fetch functions #
	def fetch_avail_port(self):
		self.cleanse_transfers()
		port = 7430

		if len(self.TRANSFERS) == 0:
			return 7430

		
		for i in range(len(self.TRANSFERS)):
			if self.TRANSFERS[i].isAlive:
				port += 1
			else:
				break

		return port

	def fetch_avail_space(self):
		return psutil.disk_usage('/').free

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

	# write_mode = "wb" write bytes "ab" append bytes
	# might want to add a check here to add a number if
	# the filename exists, to prevent data from being
	# overwritten
	def add_file(self, user, path, file_name, data, write_mode):
		if os.path.exists('Data' + '/' + user + '/' + path):
			f = open('Data' + '/' + user + '/' + path + '/' + file_name, write_mode)
			f.write(data)
			f.close()
		else:
			self.add_folder(user, path)
			self.add_file(user, path, file_name, data, write_mode)


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