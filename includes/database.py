import mysql.connector.pooling
from datetime import datetime
from includes import utils

class Database:
	def __init__(self):
		self.config = utils.fetchConfig("db.mconf")

		self.conn_pool = mysql.connector.pooling.MySQLConnectionPool(
				pool_size=int(self.config['PoolSize']),
				pool_reset_session=True,
				user=self.config['User'],
				password=self.config['Password'],
				database=self.config['Database'],
				host=self.config['Host'],
				port=self.config['Port'],
				buffered=True)

	def __repr__(self):
		return "Pool database connected to %s" % self.config['Host']

	def __del__(self):
		try:
			del self.conn_pool
			utils.log("[DB] Removing DB pool object and class.", True)
		except:
			pass

	def commit(self, query, fields):
		conn = self.conn_pool.get_connection()

		try:
			cursor = conn.cursor()
			cursor.execute(query, fields)
			conn.commit()
			utils.log("[DB] Successfully executed the query: %s, with the fields: %s." %(query, fields), True)
		except Exception as ex:
			utils.log("[DB] Failed to execute the query: %s, with the fields: %s, because of the exception: %s" %(query, fields, ex), True)
			raise ex

		cursor.close()
		conn.close()

	def queryFileAddition(self, userName, machineId, path, size, fileName):
		query = ("INSERT INTO files"
			"(UserName, NodeId, Lastmodified, Path, Size, Filename)"
			"VALUES (%s, %s, %s, %s, %s, %s)")
		query_fields = (str(userName).rstrip(), str(machineId).rstrip(), datetime.now(), path, size, str(fileName).rstrip())

		self.commit(query, query_fields)

	def queryFileDeletion(self, machineId, userName, path, fileName):
		query = "DELETE FROM files WHERE UserName = %s AND Path = %s AND Filename = %s AND NodeId = %s"
		query_fields = (str(userName).rstrip(), path, str(fileName).rstrip(), str(machineId).rstrip())

		self.commit(query, query_fields)

	def queryUserAdd(self, userName, password):
		query = ("INSERT INTO users (UserName, Password) VALUES (%s, %s)")
		query_fields = (str(userName).rstrip(), str(password).rstrip())

		self.commit(query, query_fields)

	def queryGatherUser(self, userName, password):
		conn = self.conn_pool.get_connection()
		cursor = conn.cursor()

		query = ("SELECT * FROM users WHERE UserName = %s AND Password = %s")
		query_fields = (str(userName).rstrip(), str(password).rstrip())

		cursor.execute(query, query_fields)
		conn.commit()
		data = cursor.fetchone()

		cursor.close()
		conn.close()

		return data

	def queryGatherFiles(self, userName):
		conn = self.conn_pool.get_connection()
		cursor = conn.cursor()

		query = ("SELECT * FROM files WHERE UserName = %s")

		cursor.execute(query, (str(userName).rstrip(),))
		conn.commit()

		data = cursor.fetchall()

		cursor.close()
		conn.close()

		return data

	def queryGatherSpecificFile(self, userName, fileName):
		conn = self.conn_pool.get_connection()
		cursor = conn.cursor()

		query = ("SELECT * FROM files WHERE UserName = %s AND Filename = %s")

		cursor.execute(query, (str(userName).rstrip(), fileName))
		conn.commit()

		data = cursor.fetchall()

		cursor.close()
		conn.close()

		return data

	def queryNodeProgress(self, userName, nodeId, fileName, progress):
		query = ("UPDATE files SET NodeProgress = %s WHERE UserName = %s AND Filename = %s AND NodeId = %s")
		query_fields = (progress, userName, fileName, nodeId)

		self.commit(query, query_fields)

def password_hash(self, password):
	salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
	dk = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)

	hashed_pass = dk.hex()
	return hashed_pass



def stored_hash(self, userName, password):
	# cursor = self.CONN.cursor()

	# query = ("SELECT * FROM users where = %s AND Password = %s")
	# query_fields = (userName, password_hash(password))

	#cursor.execute(query, query_fields)
	pass