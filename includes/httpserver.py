# https://docs.python.org/3/library/http.server.html
# https://stackoverflow.com/questions/31371166/reading-json-from-simplehttpserver-post-data

class RequestHandler(SimpleHTTPRequestHandler):
	def do_HEAD(self):
		pass

	def do_GET(self):
		pass

	def do_POST(self):
		pass