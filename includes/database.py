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

		ret = cursor.fetchone()[0]

		cursor.close()
		return ret

	def queryFileId(self, machineId, userName, path, filename):
		userId = self.queryUserId(userName)

		if userId == None:
			print("[DB] Invalid userName provided to queryFileId...")
			return

		cursor = self.CONN.cursor()

		query = ("SELECT FileId FROM files WHERE UserId = %s AND Path = %s AND Filename = %s AND NodeId = %s")
		query_fields = (userId, path, filename, machineId)

		cursor.execute(query, query_fields)

		ret = cursor.fetchone()
		cursor.close()

		return ret

	def queryFileAddition(self, userName, machineId, path, size, fileName):
		userId = self.queryUserId(userName)

		if userId == None:
			print("[DB] Invalid userName provided to queryFileAddition...")
			raise ValueError

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

	def queryFileDeletion(self, machineId, userName, path, filename):
		fileId = self.queryFileId(machineId, userName, path, filename)

		if fileId == None:
			print("[DB] Could not fetch a appropriate fileId")
			raise ValueError

		cursor = self.CONN.cursor()

		query = "DELETE FROM files WHERE FileId = %s"

		try:
			cursor.execute(query, (fileId))
			self.CONN.commit()
		except Exception as ex:
			print("[DB] Could not commit the deletion to the database. Exception %s" % ex)

		cursor.close()

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

	def queryRemoveFolderContents(self, machineId, userName, path):
		cursor = self.CONN.cursor()


		query = ("")

