from includes import fileops
from includes import packets
from includes import database as db
from includes import utils
from _thread import *
import socket
import threading 
import time
import json

class NodeFileHandler(threading.Thread):
	def __init__(self, mode, host, port, fileName, path, userName, msgLen, overwrite):
		self.MODE = mode
		self.MID = utils.fetch_mid()
		self.DB = None
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

			print("[NODE] Opened a NodeFileHandler socket on %s" % repr(self) + " waiting on connection...")	
		except:
			print("[NODE] Failed to open a NodeFileReceiver socket on " + repr(self))

		try:
			self.DB = db.Database("192.168.1.240", "8159", "root", "lol123", "meshdep")
			print("[NODE] Established a database connection for file operation.")
		except:
			print("[NODE] Failed to open a database connection. Can not proceed with file transfer")
			self.SOCK.close()


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
			return

		if self.CLIENT == None or self.ADDR == None:
			print("[NODE] Socket connection does not exist...")
			return
		
		if self.MODE == "SEND":
			self.exec_send()
			return
		if self.MODE == "RECV":
			self.exec_receive()
			return

		print("[NODE] Invalid mode was specified in NodeFileHandler. Returning...")

	def exec_receive(self):
		fa = fileops.FileAdder(self.USER, self.FILENAME, self.PATH)
		tbytes = 0

		try:
			while tbytes < self.LENGTH:
				recv = self.CLIENT.recv(32768)
				fa.write(recv)
				tbytes += 32768

			fa.close()
			print("Successfully received file %s" % repr(fa))
			# query the database that it was added
		except ConnectionResetError:
			print("[NODE] NodeFileReceiver socket closed.")

	def exec_send(self):
		try:
			f = open("Data/%s/%s/%s" % (self.USER, self.PATH, self.FILENAME), "rb")

			data = f.read(32768)

			while data:
				self.CLIENT.send(data)
				data = f.read(32768)

			print("[NODE] Successfully sent the file %s to server to be relayed to %s" % (self.FILENAME, self.USER))
		except Exception as ex:
			print("[NODE] Could not complete transfer, exception: %s" % ex)
			return
