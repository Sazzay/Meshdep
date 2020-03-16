import flask
#from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
import json
import threading
import os

class HTTPInstance:
	def __init__(self, ip, port, db):
		self.IP = ip
		self.PORT = port
		self.DB = db
		
		self.APP = flask.Flask("meshdep", template_folder="html")
		
		@self.APP.route('/')
		def index():
			return flask.render_template("index.html")

		@self.APP.route('/api/register', methods=['POST'])
		def register():
			return "Test"

		@self.APP.route('/api/login', methods=['POST'])
		def login():
			data = json.loads(flask.request.data)
			user = data['user']
			password = data['pass']

			#if (self.DB.queryGatherUser(user, password)):
			#	return "Test"

			test = self.DB.test()

			if(True):
				return "Test"
			
			return "Ej test"

		self.APP.run(debug=True)

	def __repr__(self):
		pass

	def __del__(self):
		print("[HTTP] Shutting down the server...")
		self.SERVER.socket.close()