# the server class,
# will run the server

from includes import serverfilehandler
from includes import database
from includes import nodeserver
from includes import utils
#from includes import httpserver
import time
import os

print("[SERVER] Starting the Database & NodeServer...")

ACTIVE = True
db = database.Database("81.170.171.18", "8159", "johan", "oq29pqxe", "meshdep")
ns = nodeserver.NodeServer("127.0.0.1", "6220", 3)
#hs = httpserver.RequestHandler(db)

db.queryFileAddition("ServerRobban", utils.fetch_mid(), "Mina Coola Bilar", 5110, "volvo740.jpg")

test = ns.NHT.find_node(60)
test.send_del_req("ServerRobban", "Mina Coola Bilar", "volvo740.jpg")

#test = ns.NHT.find_node_by_mid("36D56B8A-AB72-AFB5-46C4-049226D12DCD")
#print(test)

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

while ACTIVE:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        print("[INTERRUPT] KeyboardInterrupt detected, halting DB and Server.")
        del db
        del ns
        ACTIVE = False
        
