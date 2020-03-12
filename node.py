from includes import nodeclient
from includes import nodefilehandler
from includes import packets
import json
import time

print("[NODE] Node starting...")

HOST = "127.0.0.1"
PORT = "6220"
nc = nodeclient.NodeClient(HOST, PORT)

while True:
	try:
		recv = nc.SOCK.recv(1024)
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
			tid = pckt[6]

			thread = nodefilereceiver.NodeFileHandler(pckt[0], HOST, port, pckt[1], pckt[2], pckt[3], pckt[4], pckt[5])
			thread.start()

			nc.TRANSFERS.append(thread)
			nc.send_transfer_resp(tid, port)
	except Exception as ex:
		print("[NODE] Exception raised while receiving a packet: %s" % ex.args[0])
		break
