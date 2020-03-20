from includes import nodeclient
from includes import nodefilehandler
from includes import packets
from includes import fileops
from includes import utils
from includes import database
import json
import time

utils.log("[NODE] Node starting...", True)

config = utils.fetchConfig("node.mconf")
nc = nodeclient.NodeClient(config['Remote'], config['RemotePort'])
db = database.Database()

while True:
	try:
		recv = nc.SOCK.recv(1024)
	except ConnectionResetError:
		utils.log("[NODE] The remote socket closed the connection.", True)
		break

	try:
		rtype = packets.Packets(json.loads(recv.decode())[0])

		if rtype == packets.Packets.REQ_SPACE:
			nc.send_space_resp()

		if rtype == packets.Packets.REQ_TRANSFER:
			pckt = json.loads(recv.decode())[1]
			port = nc.fetch_avail_port()
			tid = pckt[6]

			thread = nodefilehandler.NodeFileHandler(pckt[0], config['IP'], port, pckt[1], pckt[2], pckt[3], pckt[4], pckt[5], db)
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
	except Exception as ex:
		utils.log("[NODE] Exception raised while receiving a packet: %s" % ex.args[0], True)
		break

del db