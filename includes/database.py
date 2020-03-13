import mysql.connector
from datetime import datetime
from includes import utils

class Database:
	def __init__(self, ip, port, user, password, database):
		self.IP = ip
		self.PORT = port
		self.DB = database
		self.USER = user
		self.PASS = password

		try:
			self.CONN = mysql.connector.connect(
				user=self.USER, 
				password=self.PASS,
				host=self.IP,
				port = self.PORT,
				database=self.DB)

			print("[DB] Connection to - %s was successful." % repr(self) )
		except:
			print("[DB] Connection failed.")
			kill(self)

	def __repr__(self):
		return "IP: %s PORT: %s DB: %s" % (self.IP, self.PORT, self.DB)

	def __del__(self):
		try:
			self.CONN.close()
			print("[DB] DB connection halted.")
		except:
			print("[DB] DB connection halting process failed.")

	def queryUserId(self, userName):
		cursor = self.CONN.cursor()
		query = "SELECT UserId FROM users WHERE UserName = %s"
		cursor.execute(query, (userName,))
		return cursor.fetchone()[0]

	def queryFileAddition(self, userName, machineId, path, size, fileName):
		userId = self.queryUserId(userName)

		if userId == None:
			print("[DB] Invalid userName provided to queryFileAddition...")
			return

		cursor = self.CONN.cursor()

		query = ("INSERT INTO files"
			"(UserId, NodeId, Lastmodified, Path, Size, Filename)"
			"VALUES (%s, %s, %s, %s, %s, %s)")

		query_fields = (userId, machineId, datetime.now(), path, size, fileName)

		try:
			cursor.execute(query, query_fields)
			self.CONN.commit()
		except:
			print("[DB] Could not commit the file to the database.")

		cursor.close()
		

	def queryFileDeletion(self, userName, machineId, path, fileName):
		userId = self.queryUserId(userName)

		if userId == None:
			print("[DB] Invalid userName provided to queryFileAddition...")
			return

		cursor = self.CONN.cursor()

		query = ("DELETE ")

	def queryFileMove(self):
		# this function should query the database to
		# alter the path of a file.
		pass

	def queryUserAdd(self, userName, password):
		cursor = self.CONN.cursor()

		query = ("INSERT INTO Users "
			"(UserName, Password)"
			"VALUES (%(UserName)s, %(Password)s)")

		query_fields = (userName, password)

	def queryGatherUser(self, userName, password):
		cursor = self.CONN.cursor()

		query = ("SELECT EXISTS(SELECT * FROM users WHERE"
				"(UserName, Password) ="
				"VALUES (%s, %s))")
		query_fields = (userName, password)
		cursor.execute(query, query_fields)
		
		if (cursor.fetchone() == None):
			#No hit in DB, return False
			cursor.close()
			return False
		else:
			cursor.close()
			return True

