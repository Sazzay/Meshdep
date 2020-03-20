from datetime import datetime
import os
import platform
import subprocess
import psutil
import json

def fetchConfig(confName):
	if (confName != "db.mconf" and confName != "node.mconf" and confName != "server.mconf"):
		raise ValueError("the configuration %s is invalid. Valid names are: db.mconf, node.mconf and server.mconf. Find default templates on https://github.com/Sazzay/Meshdep/wiki/Config-templates" % confName)

	data = None

	with open("conf/%s" % confName, "r") as f:
		lines = f.readlines()
		string = ""


		for i in range(len(lines)):
			string += lines[i]

	return json.loads(string)

def log(string, boolean):
	f = open("log.txt", "a")

	f.write("[" + str(datetime.now()) + "] - " + string + "\n")

	if boolean == True:
		print(string)
	
	f.close()

def fetch_avail_space():
	return psutil.disk_usage('/').free

def fetch_mid():
	if platform.system() == "Linux":
		try:
			return str(os.popen("cat /etc/machine-id").read()).rstrip()
		except:
			log("[NODE] There was an error trying to fetch /etc/machine-id.", True)


	if platform.system() == "Windows":
		try:
			return subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
		except:
			log("[NODE] Subprocess WMIC failed to fetch /etc/machine-id UUID equilivent.", True)