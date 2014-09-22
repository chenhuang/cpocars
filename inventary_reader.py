#! /usr/bin/python
# Read current and sold car inventory and print out in html

import sys
import os
import re

import json
import benz_cpo_monitor
import volvo_cpo_monitor

# Input: file name
fin = open(sys.argv[1],"r")
content = fin.read()
fin.close()

data_json = json.loads(content)
html_content = """
<!DOCTYPE html>
<html>
<head>
	<title>Benz Class</title>
	<style type="text/css">
		body {
			font-family:"Segoe UI", "Liberation Sans", "Nimbus Sans L", Helvetica, Arial, serif;
			font-size:14px;
		}

		dl {
		    margin-bottom:0px;
		}
	 
		dl dt {
		    color:#000;
		    font-weight: bold;
		    float:left; 
		    margin-right:0px; 
		    padding:0px;  
		    width: 75px;
		}
		 
		dl dd {
		    margin:0px; 
		    padding:0px;
		}
		ol,ul {
			margin:0px;
			margin-bottom: 0px;
		}
	</style>
</head>

<body>
<ol>
"""

for vehicle in data_json:
	html_content += benz_cpo_monitor.generate_email_content(vehicle)

html_content += """
</ol>

</body>
</html>
"""

print html_content




