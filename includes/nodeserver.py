import socket
from _thread import *
import threading 
import time

class NodeHandler(threading.Thread):
	def __init__(self, socket):
		self.SOCK = socket
		threading.Thread.__init__(self)

	def run(self):
		while True:
			client, addr = self.SOCK.accept()
			nt = NodeThread(client, addr)
			nt.start()

class NodeThread(threading.Thread):
	def __init__(self, client, address):
		self.CLIENT = client
		self.ADDRESS = address
		threading.Thread.__init__(self)

	def run(self):
		# send a packet back to the machine
		# and ask it to submit it's /etc/machine-id
		# 
		# after this has been done, we need to
		# find some way to link commands togheter
		# from the http server
		pass

class NodeServer:
	def __init__(self, host, port, peers):
		self.HOST = host
		self.PORT = int(port)
		self.PEERS = int(peers)

		try:
			self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.SOCK.bind((self.HOST, self.PORT))
			self.SOCK.listen(self.PEERS)

			self.NHT = NodeHandler(self.SOCK)
			self.NHT.daemon = True
			self.NHT.start()

			print("[SERVER] Opened a NodeHandler & socket on " + repr(self))	
		except:
			print("[SERVER] Failed to open a socket on " + repr(self))

	def __repr__(self):
		return "NodeServer: %s:%s" % (self.HOST, self.PORT)

	def __del__(self):
		print("[SERVER] %s shutting down" % repr(self))

