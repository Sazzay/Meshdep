from enum import Enum
import json

class Packets(str, Enum):
	HANDSHAKE = "HANDSHAKE"
	START_TRANSFER = "START_TRANSFER"
	END_TRANSFER = "END_TRANSFER"
	APP_FILE = "APP_FILE"
	RM_FILE = "RM_FILE"
	ADD_FOLDER = "ADD_FOLDER"
	RM_FOLDER = "RM_FOLDER"
	REQ_FILE = "REQ_FILE"
	REQ_SPACE = "REQ_SPACE"
	RESP_SPACE = "RESP_SPACE"

def fetchReqPacket(packetType):
	if (isinstance(packetType, Packets)):
		return json.dumps([packetType])
	else:
		print("[PACKETS] Packets type mismatch.")

def fetchSmallPacket(packetType, data):
	if (isinstance(packetType, Packets)):
		return json.dumps([packetType, data])
	else:
		print("[PACKETS] Packets type mismatch.")

def fetchFilePackets(packetType, userName, fileName, path, msgLen, data):
	if isinstance(data, str):
		data = bytearray(data, 'utf-8')

	if (not isinstance(packetType, Packets)):
		raise ValueError

	si = 0
	subdata = []
	chunks = []

	for i in range(len(data)):
		if (i % (60-len(packetType)-len(msgLen)-len(userName)-len(fileName)-len(path))) == 0 and i != 0:
			chunks.append(json.dumps([packetType, userName, fileName, path, msgLen, subdata]))
			subdata.clear()
		
		subdata.append(data[i])

	if len(subdata) > 0:
		chunks.append(json.dumps([packetType, userName, fileName, path, msgLen, subdata]))

	return chunks