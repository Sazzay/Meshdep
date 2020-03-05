from includes import packets
from _thread import *
import socket
import threading 
import time
import json

class NodeHandler(threading.Thread):
	def __init__(self, socket):
		self.THREADS = []
		self.SOCK = socket
		threading.Thread.__init__(self)

	def __repr__(self):
		return self.THREADS

	def run(self):
		while True:
			client, addr = self.SOCK.accept()
			nt = NodeThread(client, addr)
			nt.start()

			# add the thread to a list of
			# threads to be able to execute
			# commands on the thread

	def find_node(self):
		# find the most suitable node
		# by contacting each individual
		# node through their threads
		# in self.THREADS and requesting
		# the amount of available storage
		pass

class NodeThread(threading.Thread):
	def __init__(self, client, address):
		self.SUB_THREADS = []
		self.CLIENT = client
		self.ADDRESS = address
		self.MID = None
		threading.Thread.__init__(self)

		print("[SERVER] Received a new node from %s" % repr(self.ADDRESS))

	def run(self):
		# send a packet back to the machine
		# and ask it to submit it's /etc/machine-id
		# 
		# after this has been done, we need to
		# find some way to link commands togheter
		# from the http server
		while True:
			recv = self.CLIENT.recv(64)

			try:
				rtype = packets.Packets(json.loads(recv.decode())[0])
				msglen = json.loads(recv.decode())[1]

				if (rtype == packets.Packets.INIT):
					self.handshake(rtype, msglen)
			except:
				print("Test")

	def handshake(self, rtype, msglen):
		recv = self.CLIENT.recv(msglen)
		print("[SERVER] Handshake resulted in MID: %s" % recv.decode())

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

