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

	def cleanse_nodes(self):
		threads = []

		for i in range(len(self.THREADS)):
			if self.THREADS[i].isAlive():
				threads.append(self.THREADS[i])

		self.THREADS = threads

	def run(self):
		while True:
			client, addr = self.SOCK.accept()
			nt = NodeThread(client, addr)
			nt.start()

			self.THREADS.append(nt)
			nt.send_transfer_req("test", "test", "serverrobban", "50000", "False")
			nt.send_transfer_req("test0", "test0", "serverrobban", "500000", "False")
			nt.send_transfer_req("test", "test", "serverrobban", "50000", "False")
			nt.send_transfer_req("test0", "test0", "serverrobban", "500000", "False")
			nt.send_transfer_req("test", "test", "serverrobban", "50000", "False")
			nt.send_transfer_req("test0", "test0", "serverrobban", "500000", "False")

	def find_node(self):
		# always keep cleanse_nodes to purge dead threads
		# at the top of the functions
		self.cleanse_nodes()

		space = {}

		for i in range(len(self.THREADS)):
			self.THREADS[i].send_space_req()

			while self.THREADS[i].SPACE == 0 or self.THREADS[i].MID == None:
				time.sleep(0.1)

			space[self.THREADS[i].MID] = self.THREADS[i].SPACE
			self.THREADS[i].SPACE = 0

		space = {k: v for k, v in sorted(space.items(), key=lambda item: item[1])}

		print("[SERVER] Found the most suitable node as %s" % list(space.keys())[len(space)-1])

		for i in range(len(self.THREADS)):
			if list(space.keys())[len(space)-1] == self.THREADS[i].MID:
				return self.THREADS[i]

		return None
		
class NodeThread(threading.Thread):
	def __init__(self, client, address):
		self.CLIENT = client
		self.ADDRESS = address
		self.TRANSFERS = []
		self.MID = None
		self.SPACE = 0
		self.TEST = 0
		threading.Thread.__init__(self)

	def run(self):
		while True:
			try:
				recv = self.CLIENT.recv(1024)
			except ConnectionResetError:
				print("[SERVER] Connection to node %s lost." % repr(self.ADDRESS))
				break

			try:
				rtype = packets.Packets(json.loads(recv.decode())[0])

				if (rtype == packets.Packets.HANDSHAKE):
					self.recv_handshake(recv)
				if (rtype == packets.Packets.RESP_SPACE):
					self.recv_space(recv)
				if (rtype == packets.Packets.RESP_TRANSFER):
					self.recv_transfer_resp(recv)
				# add the other types below
			except Exception as ex:
				print("[SERVER] Exception raised in thread: %s" % ex.args[0])

	def fetch_transfer_port(self):
		if len(self.TRANSFERS) == 0:
			return None
		else:
			return self.TRANSFERS.pop(0)

	def recv_handshake(self, data):
		self.MID = json.loads(data.decode())[1]
		print("[SERVER] Got a new node, handshake with %s resulted in MID: %s" % (repr(self.ADDRESS), self.MID))

	def recv_space(self, data):
		self.SPACE = json.loads(data.decode())[1]
		print("[SERVER] Received a response with available node space: %s" % self.SPACE)

	def recv_file(self, data):
		# on file retrieval, relay
		# to appropriate channel
		# (http server)
		pass

	def recv_transfer_resp(self, data):
		self.TRANSFERS.append(json.loads(data.decode())[1])
		print("[SERVER] Received a response with an availble transfer node: %s" % json.loads(data.decode())[1])

	def send_space_req(self):
		time.sleep(0.05) # hacky way to avoid SOCK_STREAM polluting the recv of the node, might want to alter in future
		self.CLIENT.send((packets.fetchReqPacket(packets.Packets.REQ_SPACE)).encode())

	def send_transfer_req(self, fileName, path, userName, msgLen, overwrite):
		time.sleep(0.05) # hacky way to avoid SOCK_STREAM polluting the recv of the node, might want to alter in future
		data = [fileName, path, userName, msgLen, overwrite]
		self.CLIENT.send((packets.fetchSmallPacket(packets.Packets.REQ_TRANSFER, data)).encode())

	def send_file(self, packet):
		# open a new socket connection to the node
		# and start transfering to that socket
		# instead of the main communication
		# socket.
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

