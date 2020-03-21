from datetime import datetime
import os
import platform
import subprocess
import psutil
import json

def doesTmpFileExist(fileName, userName):
	if os.path.isfile("tmp/" + userName + "_" + fileName):
		return True
	else:
		return False

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

def initialConfig(confType):
	if confType != "server" and confType != "node" and confType != "db":
		raise ValueError("The configuration type %s is invalid, valid types are: 'server' and 'node'" % confType)

	accept = None

	if os.path.isfile('conf/initial_%s' % confType):
			log("[CONFIG] This is the first time you run the %s module and has been marked for initial configuration, would you like to configure server.mconf before running [Y/n]?" % confType, False)
			accept = input("[CONFIG] This is the first time you run the %s module and has been marked for initial configuration, would you like to configure server.mconf before running [Y/n]?" % confType)
	else: 
		return
	
	if (accept == 'Y'):
		if not os.path.isdir('conf'):
			os.mkdir('conf')

		f = open('conf/%s.mconf' % confType, "w")
		data = None

		if confType == "server":

			log("[CONFIG] IP address (.. to listen to): ", False)
			configAddr = input("[CONFIG] IP address (.. to listen to): ")
			log("[CONFIG] Port (.. to listen to): ", False)
			configPort = input("[CONFIG] Port (.. to listen to): ")
			log("[CONFIG] Max amount of connected nodes: ", False)
			configNodes = input("[CONFIG] Max amount of connected nodes: ")

			data = '{\n"IP": "%s",\n"Port": "%s",\n"MaxNodes": "%s"\n}' % (configAddr, configPort, configNodes)

		if confType == "node":

			log("[CONFIG] IP address (.. to listen to): ", False)
			configListenAddr = input("[CONFIG] IP address (.. to listen to): ")
			log("[CONFIG] IP address (.. to connect to): ", False)
			configConnAddr = input("[CONFIG] IP address (.. to connect to): ")
			log("[CONFIG] Port (.. to connect to) ", False)
			configConnPort = input("[CONFIG] Port (.. to connect to) ")

			data = '{\n"IP": "%s",\n"Remote": "%s",\n"RemotePort": "%s"\n}' % (configListenAddr, configConnAddr, configConnPort)

		if confType == "db":
			log("[CONFIG] Database IP address to connect to: ", False)
			configAddr = input("[CONFIG] Database IP address to connect to: ")
			log("[CONFIG] Database port: ", False)
			configPort = input("[CONFIG] Database port: ")
			log("[CONFIG] Database user: ", False)
			configUser = input("[CONFIG] Database user: ")
			log("[CONFIG] Database user: ", False)
			configPass = input("[CONFIG] Database user password: ")
			log("[CONFIG] Database name: ", False)
			configName = input("[CONFIG] Database name: ")
			log("[CONFIG] Max pool size: ", False)
			configPool = input("[CONFIG] Max pool size: ")

			data = ('{\n'
			'"Host": "%s",\n'
			'"Port": "%s",\n'
			'"User": "%s",\n'
			'"Password": "%s",\n'
			'"Database": "%s",\n'
			'"PoolSize": "%s"\n'
			'}') % (configAddr, configPort, configUser, configPass, configName, configPool)

		f.write(data)
		os.remove('conf/initial_%s' % confType)

		log("[CONFIG] Configuration complete.", True)
	else:
		log("[CONFIG] Skipping configuration, if you want to configure manually check https://github.com/Sazzay/Meshdep/wiki/Config-templates", True)