from includes import serverfilehandler
from includes import database
from includes import nodeserver
from includes import utils
import time
import os
import json

config = utils.fetchConfig("server.mconf")

ns = nodeserver.NodeServer(
	config['IP'], 
	config['Port'], 
	config['MaxNodes']
	)

if not os.path.exists('jobs'):
	os.makedirs('jobs')

if not os.path.exists('tmp'):
	os.makedirs('tmp')

while True:
	for file in os.listdir('jobs'):
		try:
			if file.endswith(".mjob") and len(ns.NHT.THREADS) != 0:
				utils.log("[SERVER] Found a new job. Relaying to appropriate channel.", True)

				data = None

				with open("jobs/%s" % file, "r") as f:
					data = json.loads(f.readline())

				os.remove("jobs/%s" % file)

				if data and data['Type'] == "Upload":
					with open("tmp/%s_%s" % (data['User'], data['Filename']), "rb") as f:
						node = ns.NHT.find_node(60)
						node_ip = node.fetch_ip()
						node_port = node.fetch_transfer(
							"RECV", 
							data['Filename'], 
							data['Folder'], 
							data['User'], 
							int(data['Size']), 
							data['Overwrite']
							)

						fh = serverfilehandler.ServerFileHandler(
							"SEND", 
							node_ip, 
							node_port, 
							data['Filename'], 
							data['Folder'], 
							data['User'], 
							int(data['Size']), 
							data['Overwrite']
							)
						fh.start()

				if data and data['Type'] == "Download":
					tbytes = 0
					node = ns.NHT.find_node_by_mid(data['Node'])
					node_ip = node.fetch_ip()
					node_port = node.fetch_transfer(
						"SEND",
						data['Filename'], 
						data['Folder'], 
						data['User'], 
						int(data['Size']), 
						data['Overwrite']
						)

					fh = serverfilehandler.ServerFileHandler(
							"RECV", 
							node_ip, 
							node_port, 
							data['Filename'], 
							data['Folder'], 
							data['User'], 
							int(data['Size']), 
							data['Overwrite']
							)
					fh.start()

				if data and data['Type'] == "Delete":
					node = ns.NHT.find_node_by_mid(data['Node'])
					node.send_del_req(data['User'], data['Folder'], data['Filename'])

				if data and data['Type'] == "DeleteTmp":
					while True:
						time.sleep(10)

						try:
							os.remove("tmp/" + data['User'] + "_" + data['Filename'])
							break
						except:
							pass
		except:
			pass

	if not ns.isAlive():
		break

	time.sleep(0.05)



# TESTING SERVER ===> NODE TRANSFER #
#with open("2020-02-13-raspbian-buster-full.zip", "rb") as f:
#	filename = "2020-02-13-raspbian-buster-full.zip"
#	folder = "Mina Coola Bilar"
#	user = "ServerRobban"
#	size = os.path.getsize("2020-02-13-raspbian-buster-full.zip")
#	overwrite = "True"

#	node = ns.NHT.find_node(60)
#	node_ip = node.fetch_ip()
#	node_port = node.fetch_transfer("RECV", filename, folder, user, size, overwrite)

#	fs = serverfilehandler.ServerFileHandler("SEND", node_ip, node_port, filename, folder, user, size, overwrite)
#	fs.start()

#	data = f.read(32768)

#	while data:
#		fs.enqueue(data)
#		data = f.read(32768)
##########

# TESTING NODE ===> SERVER TRANSFER #
#with open("2020-02-13-raspbian-buster-full_received.zip", "wb") as f:
#	filename = "2020-02-13-raspbian-buster-full.zip"
#	folder = "Mina Coola Bilar"
#	user = "ServerRobban"
#	size = 2653723839
#	overwrite = "True"

#	node = ns.NHT.find_node(60)
#	node_ip = node.fetch_ip()
#	node_port = node.fetch_transfer("SEND", filename, folder, user, size, overwrite)

#	fs = serverfilehandler.ServerFileHandler("RECV", node_ip, node_port, filename, folder, user, size, overwrite)
#	fs.start()

#	tbytes = 0

#	while tbytes < size:
#		f.write(fs.dequeue())
#		tbytes += 32768
##########


