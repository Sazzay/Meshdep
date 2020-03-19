from datetime import datetime
import os
import platform
import subprocess
import psutil

def get_config_val(filename, key):
	try:
		file = open(filename)

		lines = file.readline()

		while lines:
			if key in lines:
				lines = lines.partition(key)[2]
				return lines
				break
	except:
		log("utils", "No configuration file was found, creating sample configuration file...", True)
		file = open('config.txt', 'w+')
		file.write("DB_IP = 127.0.0.1\nDB_PORT = 8159\nDB_USER = root\nDB_PASS = admin\nDB_DATABASE = meshdep\n\nSERVER_IP = 127.0.0.1\nSERVER_PORT = 6220\nSERVER_MAX_NODES = 3\n\nNODE_TRANSFER_STARTPORT = 7430\n")
		return "Configuration file, config.txt, has been created. Change the default values to accurate values. "
	finally:
		file.close()

def log(prefix, string, boolean):
	f = open(prefix + "_log.txt", "a")

	if boolean == True:
		f.write(string + " -- " + str(datetime.now()) + "\n")
		print(string)
	else:
		pass
		f.close()

def fetch_avail_space():
	return psutil.disk_usage('/').free

def fetch_mid():
	if platform.system() == "Linux":
		try:
			return os.popen("cat /etc/machine-id").read()
		except:
			log("utils", "[NODE] There was an error trying to fetch /etc/machine-id.", True)

	if platform.system() == "Windows":
		try:
			return subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
		except:
			log("utils", "[NODE] Subprocess WMIC failed to fetch /etc/machine-id UUID equilivent.", True)
