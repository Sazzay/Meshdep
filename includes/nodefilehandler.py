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
	def __init__(self, mode, host, port, fileName, path, userName, msgLen, overwrite, db):
		self.MODE = mode
		self.MID = utils.fetch_mid()
		self.DB = db
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
			self.SOCK.settimeout(10)
			self.SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.SOCK.bind((self.HOST, self.PORT))
			self.SOCK.listen(1)
      
			utils.log("[NODE] Opened a NodeFileHandler socket on %s" % repr(self) + " waiting on connection...", True)	
		except:
			utils.log("[NODE] Failed to open a NodeFileReceiver socket on " + repr(self), True)

	def __repr__(self):
		return "NodeFileReceiver: %s:%s" % (self.HOST, self.PORT)

	def __del__(self):
		self.SOCK.close()
		utils.log("[NODE] %s shutting down" % repr(self), True)

	def run(self):
		try:
			self.CLIENT, self.ADDR = self.SOCK.accept()
			utils.log("[NODE] Received a file transmitter from %s" % repr(self.ADDR), True)
		except:
			utils.log("[NODE] Failed to receive a connection on file transmitter.", True)
			return

		if self.CLIENT == None or self.ADDR == None:
			utils.log("[NODE] Socket connection does not exist...", True)
			return
		
		if self.MODE == "SEND":
			self.exec_send()
			return
		if self.MODE == "RECV":
			self.exec_receive()
			return
    
		utils.log("[NODE] Invalid mode was specified in NodeFileHandler. Returning...", True)

	def exec_receive(self):
		fa = fileops.FileAdder(self.USER, self.FILENAME, self.PATH)
		tbytes = 0

		try:
			while tbytes < self.LENGTH:
				recv = self.CLIENT.recv(32768)
				fa.write(recv)
				tbytes += len(recv)

			utils.log("Successfully received file %s" % repr(fa), True)
			self.DB.queryFileAddition(self.USER, utils.fetch_mid(), self.PATH, self.LENGTH, self.FILENAME)
		except ConnectionResetError:
			utils.log("[NODE] NodeFileReceiver socket closed.", True)

		self.SOCK.close()
		fa.close()

	def exec_send(self):
		try:
			f = open("Data/%s/%s/%s" % (self.USER, self.PATH, self.FILENAME), "rb")

			data = f.read(32768)

			while data:
				self.CLIENT.send(data)
				data = f.read(32768)
        
			utils.log("[NODE] Successfully sent the file %s to server to be relayed to %s" % (self.FILENAME, self.USER), True)
		except Exception as ex:
			utils.log("[NODE] Could not complete transfer, exception: %s" % ex, True)
			return
		
		self.SOCK.close()
