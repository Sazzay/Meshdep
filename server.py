# the server class,
# will run the server

import asyncore
from includes import database
from includes import nodeserver

db = database.Database("192.168.1.240", "8159", "root", "lol123", "meshdep")
print("[SERVER] Connected to DB with " + repr(db));

nodeserver.NodeServer("127.0.0.1", "6220", 3)