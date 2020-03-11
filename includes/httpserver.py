# https://docs.python.org/3/library/http.server.html
# https://stackoverflow.com/questions/31371166/reading-json-from-simplehttpserver-post-data

class RequestHandler(SimpleHTTPRequestHandler):
	def __init__(self, conn):
		self.DB_CONN = conn
		pass

	def do_HEAD(self):
		pass

	def do_GET(self):
		pass

	def do_POST(self):
		pass