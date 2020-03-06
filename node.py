from includes import nodeclient
from includes import packets
import json
import time

print("[NODE] Node starting...")

nc = nodeclient.NodeClient("127.0.0.1", "6220")

#print("adwadwadqweqwqeqweqwdqdwqdqwdqwqwdqqwdwqwdqqwdqwqwqwdqwqdwqwdqwqdwdqw")
#test = packets.fetchFilePackets(packets.Packets.APP_FILE, "Svantesson", "stuff.jpg", "min skit", "50", "adwadwadqweqwqeqweqwdqdwqdqwdqwqwdqqwdwqwdqqwdqwqwqwdqwqdwqwdqwqdwdqw")
#test2 = ""
#print(test)
#for i in range(len(test)):
	#arr = json.loads(test[i])
#
	#for i2 in range(len(arr[5])):
	#	test2 += chr(arr[5][i2])


#print(test2)

while True:
    try:
    	recv = nc.SOCK.recv(1024)
    except ConnectionResetError:
    	print("[NODE] The remote socket closed the connection, exiting...")
    	break
    
    try:
    	rtype = packets.Packets(json.loads(recv.decode())[0])

    	if rtype == packets.Packets.REQ_SPACE:
    		nc.send_space_resp()
    except Exception as ex:
        print("[NODE] Exception raised while receiving a packet: %s" % ex.args[0])
