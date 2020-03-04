import socket
from _thread import *
import threading 
import time

class InterruptHandler(threading.Thread):
	def __init__(self, socket):
		while True:
			try:
				time.sleep(0.1)
			except KeyboardInterrupt:
				print("[SERVER] KeyboardInterrupt detected, closing the socket...")
				socket.shutdown(socket.SHUT_WR)
				return

class NodeHandler(threading.Thread):
	def __init__(self, socket):
		while True:
			client, addr = self.SOCK.accept()
			nt = NodeThread(client, addr)
			nt.start()

		self.join()


class NodeThread(threading.Thread):
	def __init__(self, client, address):
		self.CLIENT = client
		self.ADDRESS = address

		# request machine id from client next

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

			print("[SERVER] Opened a socket on " + repr(self))	
		except:
			print("[SERVER] Failed to open a socket on " + repr(self))

		try:
			self.IHT = InterruptHandler(self.SOCK).start()
			self.NHT = NodeHandler(self.SOCK).start()
		except:
			pass

	def __repr__(self):
		return "NodeServer: %s:%s" % (self.HOST, self.PORT)

