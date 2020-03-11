# the server class,
# will run the server

from includes import serverfilesender
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
with open("volvo740.jpg", "rb") as f:
	filename = "volvo740.jpg"
	folder = "Mina Coola Bilar"
	user = "ServerRobban"
	size = os.path.getsize("volvo740.jpg")
	overwrite = "True"

	node = ns.NHT.find_node(60)
	node_ip = node.ADDRESS[0]
	node_port = node.fetch_transfer(filename, folder, user, size, overwrite)

	fs = serverfilesender.FileSender(node_ip, node_port, filename, folder, user, size, overwrite)
	fs.start()

	data = f.read(1024)

	while data:
		fs.enqueue(data)
		data = f.read(1024)
##########

while ACTIVE:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        print("[INTERRUPT] KeyboardInterrupt detected, halting DB and Server.")
        del db
        del ns
        ACTIVE = False
        
