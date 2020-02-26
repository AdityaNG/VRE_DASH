# Dashboard - Vega

## Objective
The `/api/data` endpoint on the server ([http://localhost:8081/api/data](http://localhost:8081/api/data)) returns the data in JSON format.

Sample output
```json
{
   "speed":{
      "val":48.14935798577092,
      "min":0,
      "max":90,
      "unit":"Km/h"
   },
   "accelerator_pedal":{
      "val":42.810058511221804,
      "min":0,
      "max":100,
      "unit":"%"
   },
   "brake-pressure":{
      "val":130.41438644006652,
      "min":90,
      "max":130,
      "unit":"Pa"
   }
}
```
By default, it prints out the speed data it gets from the server directly to the screen and prints out all the data to the javascript console.
Your objective is to design the speedometer / dashboard in HTML that would display said data.

Feel free to make changes to index.html and index.js and add/remove files from the server folder.

*Do not remove ANY python files from the folder*

### Inputs and Pages

You may add inputs like buttons or menus to switch between different menus of the app.

Note that the entire web app should be built within one HTML page (single-page web app).

Data like speed, battery, warnings, etc should be on a main screen; while data like CAN Faults, BMS Faults, accelerator_pedal, break_pressure, steering angle, etc. should be show in one or more auxiliary menus.

Feel free to look to actual dash boards like Tesla or Ather for ideas. Think about what data might be useful on a dashboard and where you might want to place that data. *For example, speed is an important thing and is usually up front and center.*

Keep in mind, the dash will be a smartphone in horizontal orientation and with touch inputs.

## Getting Started
1. Clone this repo

2. Run ```python3 main.py```

3. Open  [http://localhost:8081/](http://localhost:8081/)  in web browser. You should see the data from the python server getting printed on the screen and the Javascript console
4. Make changes to the HTML / Js code and refresh to see changes

## Data List
A full list of all the data that you will get from `/api/data`. Note that the `val` in the data is randomly generated on the fly.
```python
DATA = {
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
```

## Submissions
Submissions should ideally be made with screenshots/videos of your working dashboard along with your *well documented code*.