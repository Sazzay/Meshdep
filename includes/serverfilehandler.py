from _thread import *
import socket
import threading 

class ServerFileHandler(threading.Thread):
	def __init__(self, mode, host, port, fileName, path, userName, msgLen, overwrite):
		self.MODE = mode
		self.DATA = []
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

			print("[SERVER] Connected to transfer node at %s" % repr(self))
		except:
			print("[SERVER] Could not connect to transfer node at %s" % repr(self))

	def __repr__(self):
		return "%s:%s" % (self.HOST, self.PORT)

	def __del__(self):
		self.SOCK.close()
		print("[SERVER] Shutting down file send operation to transfer node %s" % repr(self))

	def enqueue(self, data):
		self.DATA.append(data)

	def dequeue(self):
		while len(self.DATA) == 0:
			pass

		return self.DATA.pop(0)

	def run(self):
		if self.MODE == "SEND":
			self.exec_send()
			return

		if self.MODE == "RECV":
			self.exec_receive()
			return

		print("[SERVER] Invalid mode specified to ServerFileHandler. Returning.")

	def exec_receive(self):
		tbytes = 0

		try:
			while tbytes < self.LENGTH:
				recv = self.SOCK.recv(32768)
				self.enqueue(recv)
				tbytes += len(recv)

			print("[SERVER] Successfully received file %s from %s" % (self.FILENAME, self.HOST))
			try:
				self.SOCK.close()
			except:
				pass
		except ConnectionResetError:
			print("[NODE] NodeFileReceiver socket closed.")

	def exec_send(self):
		percentage = round(self.LENGTH / 4, 1)
		tcount = 0
		tbytes = 0

		try:
			while tbytes < self.LENGTH:
				if (tcount >= percentage):
					tcount = 0
					print("[SERVER] File transfer progress of %s for user %s to %s is %s out of %s" % (self.FILENAME, self.USER, repr(self), tbytes, self.LENGTH))

				while len(self.DATA) == 0:
					pass

				self.SOCK.send(self.DATA.pop(0))
				tcount += 32768
				tbytes += 32768

			print("[SERVER] Successfully sent file %s to %s" % (self.FILENAME, repr(self)))
			try:
				self.SOCK.close()
			except:
				pass
		except ConnectionResetError:
			print("[SERVER] File transfer operation to transfer node %s failed, remote host closed connection." % repr(self))

