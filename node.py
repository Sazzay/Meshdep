from includes import nodeclient
from includes import packets
import time

print("[NODE] Node starting...")

nc = nodeclient.NodeClient("127.0.0.1", "6220")

while True:
    try:
        recv = nc.SOCK.recv(4096)
    except KeyboardInterrupt:
        pass
