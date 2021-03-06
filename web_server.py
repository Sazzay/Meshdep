from includes import database
from includes import utils
import threading
import os
import flask
import json
import time
import re

utils.initialConfig("server")
utils.initialConfig("db")
config = utils.fetchConfig("server.mconf")

app = flask.Flask("meshdep", template_folder="html")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = database.Database()

@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
		
@app.route('/')
def index():
	if 'username' in flask.session:
		return flask.render_template("panel.html")
	else:
		return flask.render_template("index.html")

@app.route('/api/register', methods=['POST'])
def register():
	data = json.loads(flask.request.data)
	user = data['user']
	password = data['pass']

	db.queryUserAdd(user, password)

	return "Success"

@app.route('/api/login', methods=['POST'])
def login():
	data = json.loads(flask.request.data)
	user = data['user']
	password = data['pass']

	if (db.queryGatherUser(user, password)):
		flask.session['username'] = user
		return "AUTH"

	return "NAUTH"

@app.route('/api/fetch_files', methods=['GET'])
def fetch_files():
	user = flask.session['username']
	data = db.queryGatherFiles(user)

	return json.dumps(data)

@app.route('/api/upload', methods=['POST'])
def upload():
	user = flask.session['username']
	file = flask.request.files['file']

	if utils.doesTmpFileExist(user, file.filename):
		return json.dumps({'status': 'fileintransfer'})

	if (len(db.queryGatherSpecificFile(user, file.filename)) > 0):
		regExMatch = re.search('[_]\d+[.]', file.filename)

		if (regExMatch):
			s = regExMatch.span()
			file.filename = file.filename[:s[0]] + "_" + str(int(file.filename[s[0]+1:s[1]-1]) + 1)
		else:
			ss = file.filename.split(".")

			if (len(ss) >= 2):
				file.filename = ss[len(ss)-2] + "_1" + "." + ss[len(ss)-1]
			else:
				file.filename = file.filename + "_1"


		utils.log("[WEB SERVER] A naming collision occured, altered name to %s" % file.filename, True)

	file.save("tmp/" + user + "_" + file.filename)
	size = os.path.getsize("tmp/" + user + "_" + file.filename)
	overwrite = "True"

	if not os.path.exists('jobs'):
		os.makedirs('jobs')

	data = json.dumps({"Type": "Upload", "Filename": file.filename, "Folder": "", "User": user, "Size": size, "Overwrite": overwrite})

	for i in range(2000):
		if not os.path.isfile('jobs/%s.mjob' % str(i)):
			f = open('jobs/%s.mjob' % str(i), "w")
			f.write(data)
			return json.dumps({'status': 'success'})

	return json.dumps({'status': 'serveroor'})

@app.route('/api/delete', methods=['POST'])
def delete():
	post = json.loads(flask.request.data)
	user = flask.session['username']
	fileName = str(post['fileName']).rstrip()
	node = str(post['node']).rstrip()

	if not os.path.exists('jobs'):
		os.makedirs('jobs')

	data = json.dumps({"Type": "Delete", "Filename": fileName, "Folder": "", "User": user, "Node": node})

	for i in range(2000):
		if not os.path.isfile('jobs/%s.mjob' % str(i)):
			f = open('jobs/%s.mjob' % str(i), "w")
			f.write(data)
			f.close()
			return '', 200

	return '', 500

@app.route('/api/download', methods=['POST'])
def download():
	post = flask.request.form
	user = flask.session['username']
	fileName = str(post['fileName']).rstrip()
	node = str(post['node']).rstrip()
	size = post['size']
	overwrite = "True"
	timeout = 0

	if not os.path.exists('jobs'):
		os.makedirs('jobs')

	data = json.dumps({"Type": "Download", "Filename": fileName, "Folder": "", "User": user, "Node": node, "Size": size, "Overwrite": overwrite})
	
	for i in range(2000):
		if not os.path.isfile('jobs/%s.mjob' % str(i)):
			f = open('jobs/%s.mjob' % str(i), "w")
			f.write(data)
			f.close()
			break

	while True:
		if os.path.isfile("tmp/" + user + "_" + fileName):
			if os.path.getsize("tmp/" + user + "_" + fileName) >= int(size):
				break

	
	data = json.dumps({"Type": "DeleteTmp", "Filename": fileName, "User": user})

	for i in range(2000):
		if not os.path.isfile('jobs/%s.mjob' % str(i)):
			f = open('jobs/%s.mjob' % str(i), "w")
			f.write(data)
			f.close()
			break

	response = flask.make_response(flask.send_file("tmp/" + user + "_" + fileName, as_attachment=True, attachment_filename=fileName))
	response.set_cookie('fileDownload', 'true')
	response.set_cookie('path', '/')

	return response

app.run(host=config['IP'])
del db