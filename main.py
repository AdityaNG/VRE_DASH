import logging
import socketserver
from threading import Condition
from http import server
from os import curdir, sep
from urllib.parse import parse_qs
import time
import json
import random
import math
import prefs


DATA = { # Add some more data that might be useful here
	"speed": {"val":0, "min":0, "max":90, "unit": "Km/h"},
	"accelerator_pedal": {"val":0, "min":0, "max":100, "unit": "%"},
	"brake_pressure": {"val":90, "min":90, "max":130, "unit": "Pa"},
	"warning_code": {"val":0, "min":0, "max":256, "unit": "WARN"},
	"can_fault_code": {"val":0, "min":0, "max":256, "unit": "WARN"},
	"bms_fault_code": {"val":0, "min":0, "max":256, "unit": "WARN"},
	
	"battery_cell_soc_1": {"val":0, "min":0, "max":100, "unit": "%"},
	"battery_cell_soc_2": {"val":0, "min":0, "max":100, "unit": "%"},
	"battery_cell_soc_3": {"val":0, "min":0, "max":100, "unit": "%"},
	"battery_cell_soc_4": {"val":0, "min":0, "max":100, "unit": "%"},
	"battery_cell_soc_5": {"val":0, "min":0, "max":100, "unit": "%"},
	"battery_cell_soc_6": {"val":0, "min":0, "max":100, "unit": "%"},
	"battery_cell_soc_7": {"val":0, "min":0, "max":100, "unit": "%"},

	"battery_cell_temp_1": {"val":0, "min":19, "max":40, "unit": "C"},
	"battery_cell_temp_2": {"val":0, "min":19, "max":40, "unit": "C"},
	"battery_cell_temp_3": {"val":0, "min":19, "max":40, "unit": "C"},
	"battery_cell_temp_4": {"val":0, "min":19, "max":40, "unit": "C"},
	"battery_cell_temp_5": {"val":0, "min":19, "max":40, "unit": "C"},
	"battery_cell_temp_6": {"val":0, "min":19, "max":40, "unit": "C"},
	"battery_cell_temp_7": {"val":0, "min":19, "max":40, "unit": "C"},

	"motor_coil_temp_1": {"val":0, "min":19, "max":40, "unit": "C"},
	"motor_coil_temp_2": {"val":0, "min":19, "max":40, "unit": "C"},
	"motor_coil_temp_3": {"val":0, "min":19, "max":40, "unit": "C"},

	"motor_coil_current_1": {"val":0, "min":0, "max":40, "unit": "Amps"},
	"motor_coil_current_2": {"val":0, "min":0, "max":40, "unit": "Amps"},
	"motor_coil_current_3": {"val":0, "min":0, "max":40, "unit": "Amps"},

	"bms_status": {"val": 0,  "min":0, "max":3, "keys":{ 0:"OK", 1:"Temperature Warning", 2:"Battery Pack Pressure Warning", 3:"System Offline"}},
	"mcu_status": {"val": 0,  "min":0, "max":3, "keys":{ 0:"OK", 1:"APPS not connected", 2:"Motor not responding", 3:"High Voltage Fault"}},
	"vcu_status": {"val": 0,  "min":0, "max":3, "keys":{ 0:"OK", 1:"APPS not connected", 2:"MCU not responding", 3:"High Voltage Offline"}},
}

NO_INCREMENT = ("vcu_status", "mcu_status", "vcu_status")

def data_gen():
	for d in DATA:
		if d in NO_INCREMENT:
			if random.random()>0.99: # 99% chance that this data won't change
				if DATA[d]["val"]<DATA[d]["max"]:
					DATA[d]["val"]=DATA[d]["val"]+ math.floor(random.random()*10)%(DATA[d]["max"]-DATA[d]["min"])
				else:
					DATA[d]["val"] = DATA[d]["min"]
		else:
			if DATA[d]["val"]<DATA[d]["max"]:
				DATA[d]["val"]=DATA[d]["val"]+random.random()*10
			else:
				DATA[d]["val"] = DATA[d]["min"]

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
				data_gen()
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

