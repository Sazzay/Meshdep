from enum import Enum
import json

class Packets(str, Enum):
	INIT = "INIT"
	ADD_FILE = "ADD_FILE"
	RM_FILE = "RM_FILE"
	ADD_FOLDER = "ADD_FOLDER"
	RM_FOLDER = "RM_FOLDER"
	REQ_FILE = "REQ_FILE"
	EOT = "EOT" 

def sendHeader(packetType, msgLen):
	if (isinstance(packetType, Packets)):
		return json.dumps([packetType, msgLen])
	else:
		print("""
			[PACKETS] Packets module could not create a header. The
			types are a mismatch, first argument requires an enum of
			type Packets.
			""")