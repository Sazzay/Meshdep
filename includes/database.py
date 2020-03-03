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
		return (IP, PORT, USER, PASS)
