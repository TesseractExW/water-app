from urllib import parse
import model
import numpy as np;
import urllib
import os
import json
from http.server import HTTPServer , BaseHTTPRequestHandler
from dotenv import load_dotenv, dotenv_values
load_dotenv()
port = int(os.getenv("PORT"))
address = os.getenv("SERVER_ADDRESS")

data = {}

class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type','text/html')
        self.end_headers()
        message = "<h1>Data of each water checker stations</h1>"
        message += '<table style="width:100%" border="1px">'
        message += '<tr border="1px"><th border="1px">ID</th><th border="1px">PH</th><th border="1px">TDS</th><th border="1px">Is Drinkable</th></tr>'
        for id , prop in data.items():
            message += '<tr border="1px"><th border="1px">' + str(id) + '</th>'
            for i , v in prop.items():
                if v == np.int64(0):
                    v = 'No'
                elif v == np.int64(1):
                    v = 'Yes'
                message += '<th border="1px">' + str(v) + '</th>'
            message += '</tr>'
        message += '</table>'
        self.wfile.write(message.encode())
    def do_POST(self):
        if self.path.endswith('/updatesensor'):
            content_len = int(self.headers.get('Content-Length'))
            field_data  = self.rfile.read(content_len)
            fields = parse.parse_qs(str(field_data,"UTF-8"))
            self.send_response(301)
            self.send_header('Content-Type','text/html')
            print("Updating id : " + fields['id'][0] + " ph : " + fields['ph'][0] + " tds : " + fields['tds'][0])
            id = fields['id'][0]
            data[id] = {}
            data[id]['ph'] = float(fields['ph'][0])
            data[id]['tds'] = float(fields['tds'][0])
            data[id]['drinkability'] = model.predict(data[id]['ph'],data[id]['tds'])
            self.end_headers()
            self.wfile.write(bytes("Update sensor data successful!","utf8"))
server = HTTPServer((address,port),requestHandler)

print("Processor is running on " + address + ':' + str(port))
server.serve_forever()