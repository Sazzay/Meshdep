from includes import fileops
from includes import packets
from _thread import *
import socket
import threading 
import time
import json

class NodeFileReceiver(threading.Thread):
	def __init__(self, host, port, fileName, path, userName, msgLen, overwrite):
		self.CLIENT = None
		self.ADDR = None
		self.FILENAME = fileName
		self.PATH = path
		self.USER = userName
		self.LENGTH = int(msgLen)
		self.HOST = host
		self.OVERWRITE = overwrite
		self.PORT = int(port)
		threading.Thread.__init__(self)

		try:
			self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.SOCK.bind((self.HOST, self.PORT))
			self.SOCK.listen(1)

			print("[NODE] Opened a NodeFileReceiver socket on %s" % repr(self) + " waiting on connection...")	
		except:
			print("[NODE] Failed to open a NodeFileReceiver socket on " + repr(self))


	def __repr__(self):
		return "NodeFileReceiver: %s:%s" % (self.HOST, self.PORT)

	def __del__(self):
		self.SOCK.close()
		print("[NODE] %s shutting down" % repr(self))

	def run(self):
		try:
			self.CLIENT, self.ADDR = self.SOCK.accept()
			print("[NODE] Received a file transmitter from %s" % repr(self.ADDR))
		except:
			print("[NODE] Failed to receive a connection on file transmitter.")
		
		fa = fileops.FileAdder(self.USER, self.FILENAME, self.PATH)
		tbytes = 0

		while tbytes < self.LENGTH:
			try:
				recv = self.CLIENT.recv(1024)
				fa.write(recv)
				tbytes += 1024
			except ConnectionResetError:
				print("[NODE] NodeFileReceiver socket closed.")
				break

		fa.close()
		print("Successfully received file %s" % repr(fa))
