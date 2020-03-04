# the server class,
# will run the server

from includes import database

db = database.Database("192.168.1.240", "8159", "root", "lol123", "meshdep")
print("[SERVER] Connected to " + repr(db));