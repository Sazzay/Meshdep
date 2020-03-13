from includes import packets
from _thread import *
import socket
import threading 
import time
import json
# NodeServer -> NodeHandler -> NodeThread
class NodeHandler(threading.Thread):
	def __init__(self, socket):
		self.THREADS = []
		self.SOCK = socket
		threading.Thread.__init__(self)

	def __repr__(self):
		return self.THREADS

	def close_all_threads(self):
		for i in range(len(self.THREADS)):
			self.THREADS[i].CLIENT.close()

	def cleanse_nodes(self):
		threads = []

		for i in range(len(self.THREADS)):
			if self.THREADS[i].isAlive():
				threads.append(self.THREADS[i])

		self.THREADS = threads

	def run(self):
		while True:
			try:
				client, addr = self.SOCK.accept()
				nt = NodeThread(client, addr)
				nt.start()
			except:
				self.close_all_threads()
				break

			self.THREADS.append(nt)

	def find_node(self, attempts):
		# always keep cleanse_nodes to purge dead threads
		# at the top of the functions
		self.cleanse_nodes()

		if len(self.THREADS) == 0:
			while attempts > 0:
				if len(self.THREADS) > 0:
					break

				attempts -= 1
				time.sleep(0.5)

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

	def find_node_by_mid(self, mid):
		for i in range(len(self.THREADS)):
			if self.THREADS[i].MID == mid:
				return self.THREADS[i]

		return None
			
		
class NodeThread(threading.Thread):
	def __init__(self, client, address):
		self.SPACE_BUSY = False
		self.TRANSFER_BUSY = False
		self.DEL_BUSY = False
		self.CLIENT = client
		self.ADDRESS = address
		self.TRANSFERS = []
		self.MID = None
		self.TID = 0
		self.SPACE = 0
		threading.Thread.__init__(self)

	def run(self):
		while True:
			try:
				recv = self.CLIENT.recv(1024)
			except ConnectionResetError:
				print("[SERVER] Connection to node %s lost." % repr(self.ADDRESS))
				break
			except ConnectionAbortedError:
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

	def generate_tid(self):
		self.TID += 1

		if (self.TID >= 2000):
			self.TID = 0

		return self.TID

	def fetch_ip(self):
		return self.ADDRESS[0]

	def fetch_transfer(self, mode, fileName, path, userName, msgLen, overwrite):
		while self.SPACE_BUSY or self.TRANSFER_BUSY or self.DEL_BUSY:
			pass

		self.TRANSFER_BUSY = True
		tid = self.generate_tid()
		data = [mode, fileName, path, userName, msgLen, overwrite, tid]
		self.CLIENT.send((packets.fetchSmallPacket(packets.Packets.REQ_TRANSFER, data)).encode())

		attempts = 0

		while attempts < 60:
			for i in range(len(self.TRANSFERS)):
				if str(tid) in self.TRANSFERS[i]:
					ret = self.TRANSFERS[i].get(str(tid))
					del self.TRANSFERS[i]
					print(self.TRANSFERS)
					return ret

			attempts += 1
			time.sleep(0.5)

		print("[SERVER] Could not fetch a transfer subnode from the node.")

	def recv_handshake(self, data):
		self.MID = json.loads(data.decode())[1]
		print("[SERVER] Got a new node, handshake with %s resulted in MID: %s" % (repr(self.ADDRESS), self.MID))

	def recv_space(self, data):
		self.SPACE_BUSY = False
		self.SPACE = json.loads(data.decode())[1]
		print("[SERVER] Received a response with available node space: %s" % self.SPACE)

	def recv_transfer_resp(self, data):
		self.TRANSFER_BUSY = False
		self.TRANSFERS.append(json.loads(data.decode())[1])
		print("[SERVER] Received a response with an availble transfer node: %s" % json.loads(data.decode())[1])

	def recv_del_resp(self, success):
		self.DEL_BUSY = False
		
		if success == True:
			print("[SERVER] Node reports the file deletion was successful.")
		else:
			print("[SERVER] Node reports the file deletion failed.")

	def send_space_req(self):
		while self.SPACE_BUSY or self.TRANSFER_BUSY or self.DEL_BUSY:
			pass

		self.SPACE_BUSY = True
		self.CLIENT.send((packets.fetchReqPacket(packets.Packets.REQ_SPACE)).encode())

	def send_del_req(self, data):
		while self.SPACE_BUSY or self.TRANSFER_BUSY or self.DEL_BUSY:
			pass

		self.DEL_BUSY = True

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
		self.SOCK.close()
		print("[SERVER] %s shutting down" % repr(self))

