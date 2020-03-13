import socket
from includes import packets
from includes import utils

class NodeClient:
	def __init__(self, ip, port):
		self.TRANSFERS = []
		self.ACTIVE = False
		self.IP = ip
		self.PORT = int(port)
		self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			self.ACTIVE = True
			self.SOCK.connect((self.IP, self.PORT))

			print("[NODE] Successfully established a connection to %s:%s" % (self.IP, self.PORT))
		except:
			print("[NODE] Failed to establish a connection to %s:%s" % (self.IP, self.PORT))

		self.send_handshake()

	def __repr__(self):
		return "%s:%s" % (self.IP, self.PORT)

	# send functions #
	def send_handshake(self):
		mid = utils.fetch_mid()
		self.SOCK.send((
			packets.fetchSmallPacket(
			packets.Packets.HANDSHAKE, 
			mid).encode()
			))

	def send_space_resp(self):
		space = utils.fetch_avail_space()

		self.SOCK.send((
			packets.fetchSmallPacket(
			packets.Packets.RESP_SPACE, 
			space).encode()
			))

		print("[NODE] Received a space request, sending space response: %s" % space)

	def send_transfer_resp(self, tid, port):
		# fetch an availble port based on
		# active socket threads in 

		data = {}
		data[tid] = port

		self.SOCK.send((
			packets.fetchSmallPacket(
			packets.Packets.RESP_TRANSFER, 
			data).encode()
			))

	def send_del_resp(self, success):
		pass
	# recv functions #

	# cleanse functions #
	def cleanse_transfers(self):
		transfers = []

		for i in range(len(self.TRANSFERS)):
			if self.TRANSFERS[i].isAlive():
				transfers.append(self.TRANSFERS[i])

		self.TRANSFERS = transfers

	# fetch functions #
	def fetch_avail_port(self):
		self.cleanse_transfers()
		port = 7430

		if len(self.TRANSFERS) == 0:
			return 7430

		
		for i in range(len(self.TRANSFERS)):
			if self.TRANSFERS[i].isAlive:
				port += 1
			else:
				break

		return port