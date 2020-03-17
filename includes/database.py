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

	def commit(self, query, fields):
		cursor = self.CONN.cursor()

		try:
			cursor.execute(query, fields)
			self.CONN.commit()
			print("[DB] Successfully executed the query: %s, with the fields: %s." %(query, fields))
		except Exception as ex:
			print("[DB] Failed to execute the query: %s, with the fields: %s, because of the exception: %s" %(query, fields, ex))
			raise ex

		cursor.close()

	# Returns the userId based on the userName (which is always also unique) #
	def queryUserId(self, userName):
		cursor = self.CONN.cursor()

		query = "SELECT UserId FROM users WHERE UserName = %s"

		cursor.execute(query, (userName,))

		ret = cursor.fetchone()[0]

		cursor.close()
		return ret

	# Query that returns a file id to be used when deleting or adding #
	# files 														  #
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

	# Query that returns an array of nodes that contain the path specified #
	# Eg: path is "Mina Coola Bilar" will return all nodes containing that #
	# folder and it's sub folders 										   #
	def queryNodesWithFolder(self, userName, path):
		userId = self.queryUserId(userName)

		if userId == None:
			print("[DB] Invalid userName provided to queryFileId...")
			return

		cursor = self.CONN.cursor()

		query = ("SELECT NodeId from files WHERE UserId = %s AND Path LIKE %s")
		query_fields = (userId, path + "%")

		cursor.execute(query, query_fields)
		ret = cursor.fetchall()
		cursor.close()

		arr = []

		for i in range(len(ret)):
			arr.append(ret[i][0].rstrip())

		return arr

	# Query that adds a folder for the user in the database, this can #
	# then be used to display this back to the user and then he may   #
	# use it to add files into the folder.							  #
	def queryFolderAddition(self, userName, path):
		userId = self.queryUserId(userName)

		if userId == None:
			print("[DB] Invalid userName provided to queryFileAddition...")
			raise ValueError

		query = ("INSERT INTO folders (UserId, LastModified, Path) VALUES (%s, %s, %s)")
		query_fields = (userId, datetime.now(), path)

		self.commit(query, query_fields)

	def queryFileAddition(self, userName, machineId, path, size, fileName):
		userId = self.queryUserId(userName)

		if userId == None:
			print("[DB] Invalid userName provided to queryFileAddition...")
			raise ValueError

		query = ("INSERT INTO files"
			"(UserId, NodeId, Lastmodified, Path, Size, Filename)"
			"VALUES (%s, %s, %s, %s, %s, %s)")
		query_fields = (userId, machineId, datetime.now(), path, size, fileName)

		self.commit(query, query_fields)

	def queryFileDeletion(self, machineId, userName, path, filename):
		fileId = self.queryFileId(machineId, userName, path, filename)

		if fileId == None:
			print("[DB] Could not fetch a appropriate fileId")
			raise ValueError

		query = "DELETE FROM files WHERE FileId = %s"
		query_fields = (fileId)

		self.commit(query, query_fields)

	def queryRemoveFolderContents(self, machineId, userName, path):
		userId = self.queryUserId(userName)

		if userId == None:
			print("[DB] Invalid userName provided to queryFileAddition...")
			raise ValueError

		cursor = self.CONN.cursor()

		query = ("DELETE FROM files WHERE UserId = %s AND NodeId = %s AND Path LIKE %s")
		query_fields = (userId, machineId, path + "%")

		try:
			cursor.execute(query, query_fields)
			self.CONN.commit()
			print("[DB] Removed the folders under %s with user %s" % (path, userName))
		except Exception as ex:
			print("[DB] Could not commit the deletion to the database. Exception %s" % ex)

		cursor.close()

	def queryUserAdd(self, userName, password):
		cursor = self.CONN.cursor()

		query = ("INSERT INTO Users "
			"(UserName, Password)"
			"VALUES (%(UserName)s, %(Password)s)")

		query_fields = (userName, password)

	def queryGatherUser(self, userName, password):
		cursor = self.CONN.cursor()

		query = ("SELECT * FROM users WHERE UserName = %s AND Password = %s")
		query_fields = (userName, password)

		cursor.execute(query, query_fields)
		hit = cursor.fetchone()

		cursor.close()

		return hit

	def queryGatherFiles(self, userName):
		userId = self.queryUserId(userName)

		if userId == None:
			print("[DB] Invalid userName provided to queryFileAddition...")
			raise ValueError

		cursor = self.CONN.cursor(buffered=True)

		query = ("SELECT * FROM files WHERE UserId = %s")

		cursor.execute(query, (userId,))
		self.CONN.commit()

		data = cursor.fetchall()

		cursor.close()

		print(len(data))

		return data



