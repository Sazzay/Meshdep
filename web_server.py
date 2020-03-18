from includes import database
import os
import flask
import json

db = database.Database("81.170.171.18", "8159", "johan", "oq29pqxe", "meshdep")

app = flask.Flask("meshdep", template_folder="html")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
	# should try to add the values provided
	# in the request (that is username and
	# password) into the database using 
	# db.queryUserAdd
	pass

@app.route('/api/login', methods=['POST'])
def login():
	data = json.loads(flask.request.data)
	user = data['user']
	password = data['pass']

	if (db.queryGatherUser(user, password)):
		flask.session['username'] = user
		return "AUTH"

	return "NAUTH"

@app.route('/api/upload', methods=['POST'])
def upload():
	user = flask.session['username']
	file = flask.request.files['file']
	file.save("tmp/" + user + "_" + file.filename)
	size = os.path.getsize("tmp/" + user + "_" + file.filename)
	overwrite = "True"

	if not os.path.exists('jobs'):
		os.makedirs('jobs')

	data = json.dumps({"Type": "Upload", "Filename": file.filename, "Folder": "", "User": user, "Size": size, "Overwrite": overwrite})

	for i in range(500):
		if not os.path.isfile('jobs/%s.mjob' % str(i)):
			f = open('jobs/%s.mjob' % str(i), "w")
			f.write(data)
			return json.dumps("Success")


	return json.dumps("Failed, exceeded the maximum amount of queued jobs")

@app.route('/api/fetch_files', methods=['GET'])
def fetch_files():
	user = flask.session['username']
	data = db.queryGatherFiles(user)

	return json.dumps(data)



app.run(debug=True)
del db