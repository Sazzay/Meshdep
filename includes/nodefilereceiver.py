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
		self.MFT = 1
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
		print("[NODE] %s shutting down" % repr(self))

	def run(self):
		try:
			self.CLIENT, self.ADDR = self.SOCK.accept()
			print("[NODE] Received a file transmitter from %s" % repr(self.ADDR))
		except:
			print("[NODE] Failed to receive a connection on file transmitter.")
		
		tbytes = 0

		while tbytes < self.LENGTH:
			try:
				recv = self.CLIENT.recv(1024)
				tbytes += 1024
			except ConnectionResetError:
				print("[NODE] NodeFileReceiver socket closed.")
				break
