# the server class,
# will run the server

from includes import serverfilehandler
from includes import database
from includes import nodeserver
#from includes import httpserver
import time
import os

print("[SERVER] Starting the Database & NodeServer...")

ACTIVE = True
db = database.Database("192.168.1.240", "8159", "root", "lol123", "meshdep")
ns = nodeserver.NodeServer("127.0.0.1", "6220", 3)
#hs = httpserver.RequestHandler(db)

# TESTING #
with open("2020-02-13-raspbian-buster-full.zip", "rb") as f:
	filename = "2020-02-13-raspbian-buster-full.zip"
	folder = "Mina Coola Bilar"
	user = "ServerRobban"
	size = os.path.getsize("2020-02-13-raspbian-buster-full.zip")
	overwrite = "True"

	node = ns.NHT.find_node(60)
	node_ip = node.fetch_address()
	node_port = node.fetch_transfer("RECV", filename, folder, user, size, overwrite)

	fs = serverfilesender.ServerFileHandler("SEND", node_ip, node_port, filename, folder, user, size, overwrite)
	fs.start()

	data = f.read(32768)

	while data:
		fs.enqueue(data)
		data = f.read(32768)
##########

while ACTIVE:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        print("[INTERRUPT] KeyboardInterrupt detected, halting DB and Server.")
        del db
        del ns
        ACTIVE = False
        
