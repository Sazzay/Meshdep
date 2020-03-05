# the server class,
# will run the server

import asyncore
from includes import database
from includes import nodeserver
import time

print("[SERVER] Starting the Database & NodeServer...")

ACTIVE = True
db = database.Database("192.168.1.240", "8159", "root", "lol123", "meshdep")
ns = nodeserver.NodeServer("127.0.0.1", "6220", 3)

while ACTIVE:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        print("[INTERRUPT] KeyboardInterrupt detected, halting DB and Server.")
        del db
        del ns
        ACTIVE = False
        
