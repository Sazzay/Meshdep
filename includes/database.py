import mysql.connector

class Database:
	IP = "127.0.0.1"
	DB = "CloudDB"
	USER = "root"
	PASS = "admin"
	CONN = None

	def __init__(self, ip, user, password, database):
		self.IP = ip
		self.DB = database
		self.USER = user
		self.PASS = password

		try:
			CONN = mysql.connector.connect(
				user=USER, 
				password=PASS,
				host=IP,
				database=DB)
		except:
			kill(self)
			print("[DB] Connection failed.")

	def __repr__(self):
		return {'ip':self.IP, 'db':self.DB}

	def __del__(self):
		try:
			CONN.close()
		except:
			continue

	def queryFileAddition(self):
		# this function should query the database
		# to add relevant information about
		# the file that is being added to a node
		# should only be called after the node successfully
		# retrieved data.

	def queryFileDeletion(self):
		# this function should query the database
		# to delete the relevant file.

	def queryFileMove(self):
		# this function should query the database to
		# alter the path of a file.
