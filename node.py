from includes import nodeclient
from includes import nodefilehandler
from includes import packets
from includes import fileops
from includes import utils
from includes import database
import json
import time

print("[NODE] Node starting...")

HOST = "127.0.0.1"
PORT = "6220"
nc = nodeclient.NodeClient(HOST, PORT)
db = database.Database("81.170.171.18", "8159", "johan", "oq29pqxe", "meshdep")

#print(db.queryNodesWithFolder("ServerRobban", "/Mina Coola Bilar"))

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

			thread = nodefilehandler.NodeFileHandler(pckt[0], HOST, port, pckt[1], pckt[2], pckt[3], pckt[4], pckt[5], db)
			thread.start()

			nc.TRANSFERS.append(thread)
			nc.send_transfer_resp(tid, port)

		if rtype == packets.Packets.REQ_DEL:
			pckt = json.loads(recv.decode())[1]

			try:
				fileops.rm_file(pckt[0], pckt[1], pckt[2])
				db.queryFileDeletion(utils.fetch_mid(), pckt[0], pckt[1], pckt[2])
				nc.send_del_resp(True)
			except:
				nc.send_del_resp(False)
		
		if rtype == packets.Packets.REQ_ADD_FOLDER:
			pckt = json.loads(recv.decode())[1]

			try:
				fileops.add_folder(pckt[0], pckt[1])
				nc.send_add_folder_resp(True)
			except:
				nc.send_add_folder_resp(False)

		if rtype == packets.Packets.REQ_DEL_FOLDER:
			pckt = json.loads(recv.decode())[1]

			try:
				fileops.rm_folder(pckt[0], pckt[1])
				db.queryRemoveFolderContents(utils.fetch_mid(), pckt[0], pckt[1])
				nc.send_del_folder_resp(True)
			except:
				nc.send_del_folder_resp(False)
	except Exception as ex:
		print("[NODE] Exception raised while receiving a packet: %s" % ex.args[0])
		break

del db