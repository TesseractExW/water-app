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
        message = '<body style="font-family:"Lucida Console", "Courier New", monospace"'
        message += "<h1>Data of each water checker stations</h1>"
        message += '<table style="width:100%" >'
        message += '<tr style="background-color:7CC8C3;"><th>ID</th><th >PH</th><th >TDS</th><th>Drinkability</th></tr>'
        i = 0
        for id , prop in data.items():
            if i % 2 == 0:
                message += '<tr style="background-color:FCF4E4;"><th>' + str(id) + '</th>'
            else:
                message += '<tr style="background-color:BFE6D4;"><th>' + str(id) + '</th>'
            for _i,v in prop.items():
                if v == np.int64(0):
                    v = 'No'
                elif v == np.int64(1):
                    v = 'Yes'
                message += '<th>' + str(v) + '</th>'
            message += '</tr>'
            i += 1
        message += '</table>'
        message += '</body>'
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
            data[id]['drinkability'] = str(int(model.predict(data[id]['ph'],data[id]['tds'])[0]*100)) + '%'
            self.end_headers()
            self.wfile.write(bytes("Update sensor data successful!","utf8"))
server = HTTPServer((address,port),requestHandler)

print("Processor is running on " + address + ':' + str(port))
server.serve_forever()