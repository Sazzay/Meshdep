from includes import nodeclient
from includes import nodefilereceiver
from includes import packets
import json
import time

print("[NODE] Node starting...")

HOST = "127.0.0.1"
PORT = "6220"
nc = nodeclient.NodeClient(HOST, PORT)

while True:
	try:
		recv = nc.SOCK.recv(256)
	except ConnectionResetError:
		print("[NODE] The remote socket closed the connection.")
		break

	try:
		rtype = packets.Packets(json.loads(recv.decode())[0])

		if rtype == packets.Packets.REQ_SPACE:
			nc.send_space_resp()
		if rtype == packets.Packets.REQ_TRANSFER:
			pckt = json.loads(recv.decode())[1]
			port = nc.fetch_avail_port()

			thread = nodefilereceiver.NodeFileReceiver(HOST, port, pckt[0], pckt[1], pckt[2], pckt[3], pckt[4])
			thread.start()

			nc.TRANSFERS.append(thread)
			nc.send_transfer_resp(port)
	except Exception as ex:
		print("[NODE] Exception raised while receiving a packet: %s" % ex.args[0])
		break
