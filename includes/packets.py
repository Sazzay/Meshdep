from enum import Enum
import json
import sys

class Packets(str, Enum):
	HANDSHAKE = "HANDSHAKE"
	REQ_SPACE = "REQ_SPACE"
	RESP_SPACE = "RESP_SPACE"
	REQ_TRANSFER = "REQ_TRANSFER"
	RESP_TRANSFER = "RESP_TRANSFER"
	REQ_DEL = "REQ_DEL"
	RESP_DEL = "RESP_DEL"
	REQ_ADD_FOLDER = "REQ_ADD_FOLDER"
	REQ_DEL_FOLDER = "REQ_DEL_FOLDER"
	RESP_ADD_FOLDER = "RESP_ADD_FOLDER"
	RESP_DEL_FOLDER = "RESP_DEL_FOLDER"

def fetchReqPacket(packetType):
	if (isinstance(packetType, Packets)):
		return json.dumps([packetType])
	else:
		utils.log("[PACKETS] Packets type mismatch.", True)

def fetchSmallPacket(packetType, data):
	if (isinstance(packetType, Packets)):
		if (sys.getsizeof(data) + sys.getsizeof(packetType)) > 1024:
			utils.log("[PACKETS] The amount of data has exceeded the maximum of 1024 bytes", True)
		else:
			return json.dumps([packetType, data])
	else:
		utils.log("[PACKETS] Packets type mismatch.", True)