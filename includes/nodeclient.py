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
			utils.log("nodeclient", "[NODE] Successfully established a connection to %s:%s" % (self.IP, self.PORT), True)
		except:
			utils.log("nodeclient", "[NODE] Failed to establish a connection to %s:%s" % (self.IP, self.PORT), True)
		self.send_handshake()

	def __repr__(self):
		return "%s:%s" % (self.IP, self.PORT)

	# send functions #
	def send_handshake(self):
		mid = str(utils.fetch_mid()).rstrip()
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
		utils.log("nodeclient", "[NODE] Received a space request, sending space response: %s" % space, True)
		
	def send_transfer_resp(self, tid, port):
		data = {}
		data[tid] = port

		self.SOCK.send((
			packets.fetchSmallPacket(
			packets.Packets.RESP_TRANSFER, 
			data).encode()
			))

	def send_del_resp(self, success):
		self.SOCK.send((
			packets.fetchSmallPacket(
			packets.Packets.RESP_DEL,
			success).encode()
			))

	def send_add_folder_resp(self, success):
		self.SOCK.send((
			packets.fetchSmallPacket(
			packets.Packets.RESP_ADD_FOLDER,
			success).encode()
			))

	def send_del_folder_resp(self, success):
		self.SOCK.send((
			packets.fetchSmallPacket(
			packets.Packets.RESP_DEL_FOLDER,
			success).encode()
			))
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
