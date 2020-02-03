import logging
import socketserver
from threading import Condition
from http import server
from os import curdir, sep
from urllib.parse import parse_qs
import time
import json

import prefs


DATA = { # Add some more data that might be useful here
	"speed": 123,
	"accelerator_pedal": 255,
	"brake-pressure": 98
}

class StreamingHandler(server.BaseHTTPRequestHandler):
		def do_GET(self):
			if "/api/request?" in self.path: # This is used to accept inputs from outside
				# For example, by requesting /api/?callibrate_apps=1 we can remotely trigger the calibration
				global params
				PAGE = "{'status': ok}"
				try:
					params = parse_qs(self.path[2:])
					for d in params:
						prefs.set_pref(d, params[d][0])
						prefs.set_pref(d+ "_last_message", str(time.time()))
					
					prefs.set_pref("last_message_all", str(time.time())) # 
					print("GOT : ", params)
				except Exception as e:
					PAGE = "{'status': 'not ok', 'error': '" + str(e) + "' }"
				self.send_response(200)
				self.send_header('Content-Type', 'text/json')
				content = PAGE.encode('utf-8')
				self.send_header('Content-Length', len(content))
				self.end_headers()
				self.wfile.write(content)
			elif "/api/data" in self.path: # send data
				self.send_response(200)
				PAGE = json.dumps(DATA)
				self.send_header('Content-Type', 'text/html')
				content = PAGE.encode('utf-8')
				self.send_header('Content-Length', len(content))
				self.end_headers()
				self.wfile.write(content)
			elif self.path == '/': # Redirect / to /index.html
				self.send_response(301)
				self.send_header('Location', '/index.html')
				self.end_headers()
			else: # Try opening the requested file
				try:
					print('Opening file : ', self.path[1:])
					PAGE = ""
					self.send_response(200)
					if self.path.endswith('.png'): # Currently supports only PNG images
						f = open(self.path[1:], 'rb')
						PAGE = f.read()
						self.send_header('Content-Type', 'image/png')
						content = PAGE
					else:
						f = open(self.path[1:], 'r')
						PAGE = f.read()
						self.send_header('Content-Type', 'text/html')
						content = PAGE.encode('utf-8')
					self.send_header('Content-Length', len(content))
					self.end_headers()
					self.wfile.write(content)
				except Exception as e:
					self.send_error(404)
					self.end_headers()
					print(e)

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
	allow_reuse_address = True
	daemon_threads = True


try:
	print("Starting Arduino Server at port 8081")
	print("http://localhost:8081")
	address = ('', 8081)
	server = StreamingServer(address, StreamingHandler)
	server.serve_forever()
finally:
	print("Arduino Server ended")

