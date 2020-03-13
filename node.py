from includes import nodeclient
from includes import nodefilehandler
from includes import packets
from includes import fileops
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

			thread = nodefilehandler.NodeFileHandler(pckt[0], HOST, port, pckt[1], pckt[2], pckt[3], pckt[4], pckt[5])
			thread.start()

			nc.TRANSFERS.append(thread)
			nc.send_transfer_resp(tid, port)
		if rtype == packets.Packets.REQ_DEL:
			pckt = json.loads(recv.decode())[1]

			try:
				fileops.rm_file(pckt[0], pckt[1], pckt[2])
				print("[NODE] Deleted the requested file, sending success response...")
				nc.send_del_resp(True)
			except:
				print("[NODE] Failed to delete the requested file, sending fail response...")
				nc.send_del_resp(False)
	except Exception as ex:
		print("[NODE] Exception raised while receiving a packet: %s" % ex.args[0])
		break
