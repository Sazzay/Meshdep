from includes import utils
from _thread import *
import socket
import threading
import os

class ServerFileHandler(threading.Thread):
	def __init__(self, mode, host, port, fileName, path, userName, msgLen, overwrite):
		self.MODE = mode
		self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.FILENAME = fileName
		self.PATH = path
		self.USER = userName
		self.LENGTH = int(msgLen)
		self.HOST = host
		self.OVERWRITE = overwrite
		self.PORT = int(port)
		threading.Thread.__init__(self)

		try:
			self.SOCK.connect((self.HOST, self.PORT))

			utils.log("[SERVER] Connected to transfer node at %s" % repr(self), True)
		except:
			utils.log("[SERVER] Could not connect to transfer node at %s" % repr(self), True)

	def __repr__(self):
		return "%s:%s" % (self.HOST, self.PORT)

	def __del__(self):
		self.SOCK.close()
		utils.log("[SERVER] Shutting down file send operation to transfer node %s" % repr(self), True)

	def run(self):
		if self.MODE == "SEND":
			self.exec_send()
			return

		if self.MODE == "RECV":
			self.exec_receive()
			return

		utils.log("[SERVER] Invalid mode specified to ServerFileHandler. Returning.", True)

	def exec_receive(self):
		tbytes = 0

		try:
			with open("tmp/%s_%s" % (self.USER, self.FILENAME), "wb") as f:
				while tbytes < self.LENGTH:
					bytesWritten = f.write(self.SOCK.recv(32768))
					tbytes += bytesWritten

			utils.log("[SERVER] Successfully received file %s from %s" % (self.FILENAME, self.HOST), True)

			try:
				self.SOCK.close()
			except:
				pass
		except Exception as ex:
			utils.log("[NODE] ServerFileHandler exception occured while reciving data, reason: %s" % ex, True)

	def exec_send(self):
		tbytes = 0

		try:
			with open("tmp/%s_%s" % (self.USER, self.FILENAME), "rb") as f:
				while tbytes < self.LENGTH:
					bytesSent = self.SOCK.send(f.read(32768))
					tbytes += bytesSent

			os.remove("tmp/%s_%s" % (self.USER, self.FILENAME))

			utils.log("[SERVER] Successfully sent file %s to %s" % (self.FILENAME, repr(self)), True)

			try:
				self.SOCK.close()
			except:
				pass
		except Exception as ex:
			utils.log("[SERVER] ServerFileHandler exception occured while sending data to %s, reason: %s" % (repr(self), ex), True)

