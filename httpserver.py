from http.server import SimpleHTTPRequestHandler, HTTPServer
#from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
import json
import database


INTERFACES = 'localhost'
PORT = 8020

class RequestHandler(SimpleHTTPRequestHandler):

    responseValue = 200
    
    def _set_response(self, responseValue):
        self.send_response(responseValue)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        db = database.Database("81.170.171.18", "8159", "johan", "oq29pqxe", "meshdep")

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print(post_data.decode())

        requestType = (post_data.decode()).split('"')[3]
        userName = (post_data.decode()).split('"')[7]
        password = (post_data.decode()).split('"')[11]
        print(requestType)
        print(userName)
        print(password)
        
        if(requestType == "register"):
            try:
                db.queryUserAdd(userName, password)
                responseValue = 200
                self._set_response(responseValue)
            except:
                responseValue = 400
                self._set_response(responseValue)
            del db 
            
        elif(requestType == "login"):
            if (db.queryGatherUser(userName, password) == False):
                print("[DB] User %s does not exist" % userName)
                #skicka tillbaks att användaren också att de inte finns, försök igen
            #Ha en else/elif för att testa som försöker hämta data från Filestabellen
            elif(db.queryGatherUser(userName, password) == True):
                print("[DB] User %s logged in" % userName)
                #Redirecta användaren till UserDataTabell-htmlsidan
                #Ge ett sessionsID till användaren


            #kolla ifall inloggningsinfon finns i databasen
            #if den finns, hämta all information ur Files tabellen
                #som stämmer med inloggsinfo & skicka tbax som response
            #else det INTE finns, ge meddelande att användaren inte finns
                #reggad i db
        
            pass

        #self._set_response()
        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        
    # Override handler for GET requests
    #def do_GET(self):
     
        #self.path = '/html' + self.path
        #return super().do_GET()
    
#db = database.Database("81.170.171.18", "8159", "johan", "oq29pqxe", "meshdep")
try:
    server = HTTPServer(('localhost', PORT), RequestHandler)
    print('Starting HTTP server on http://' + 'localhost' + ":" + str(PORT))
    server.serve_forever()

except KeyboardInterrupt:
    print('Ctrl-C received, shutting down the web server')
    server.socket.close()
