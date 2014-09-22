#! /usr/bin/python
# This script monitors Mercedes Benz Preowned vehicle website and send new preowned car information whenever possible. 

import sys
import re
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP_SSL as SMTP
import httplib
import json
import os.path
import datetime

# Input Variables: zipcode and distance
# Other parameters are pretty much set: E-Class, from 2011, sorted by price. 
#zipcode = 20770
#distance = 50
#class_number = 3
class_name = {2:"C", 3:"E"}
#year_from = 2011
#year_to = 2013
working_directory = "/Users/chhuang/Dropbox/Car/"

# SMTP Email Sending Function
# Outlook.com works really great on this one
def send_email(subject, content):
	me = "email_to_send_price_update@gmail.com"
	you = "email_to_receive_price_update@gmail.com"

	SMTP_server = "smtp.gmail.com"
	user_name = me
	pwd = "password"
	SMTP_port = 587

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = me
	msg['To'] = you

	msg.attach(MIMEText(content,'html'))

	conn = smtplib.SMTP(SMTP_server,SMTP_port)
	conn.starttls()
	conn.login(user_name,pwd)
	conn.sendmail(me, you, msg.as_string())
	conn.close()

# Fetch data from MBPreowned, with the given zipcode and distance
def fetch_data(zipcode,distance,class_number, year_from, year_to):
	url = "www.mypreownedmercedes.com"
	#query = '/mbucl?search={%22country2%22:%22US%22,%22hits%22:{%22to%22:999},%22cpo%22:1,%22postcode%22:%22'	+str(zipcode)	+'%22,%22distance%22:{%22to%22:%22'	+str(distance)	+'%22},%22year%22:{%22to%22:9998},%22order%22:[%22pricea%22],%22class_bodystyle%22:[{%22class%22:3,%22bodystyle%22:[1],%22model%22:[],%22variant%22:[]}]}'
	query = '/mbucl?search={"country2":"US","hits":{"to":999},"cpo":1,"postcode":"'+str(zipcode)+'","distance":{"to":"'+str(distance)+'"},"year":{"from":"'+str(year_from)+'","to":'+str(year_to)+'},"order":["pricea"],"class_bodystyle":[{"class":'+str(class_number)+',"bodystyle":[1],"model":[],"variant":[]}]}'
	conn = httplib.HTTPConnection(url)
	conn.request("GET",query)
	rl = conn.getresponse()
	if rl.status != 200 or rl.reason != "OK":
		send_email("mypreownedmercedes web error",rl.status+": "+rl.reason)
		sys.exit(0)
	data = rl.read()
	data_json = json.loads(data)
	vehicles_data = data_json["vehicles"]

	return vehicles_data

# Update local database and send the new vehicle information to my email box
# I keep two files on record:
# 1. Current vehicle list, the list that keeps the most updated car information
# 2. Archived vehicle list, the list that keeps cars that have been sold.

def update(vehicles_data,zipcode,distance,class_number):
	on_market_file_name = working_directory + str(zipcode)+"_"+str(distance)+"_"+str(class_number)+"_current.json"
	sold_file_name = working_directory + str(zipcode) + "_" + str(distance) +"_"+str(class_number)+"_sold.json"
	data = ""
	vin_current_cars = {}
	vins_set = set()
	if os.path.isfile(on_market_file_name) == True:
		fin = open(on_market_file_name, "r")
		data = fin.read()
		fin.close()
		current_cars = json.loads(data)
		for car in current_cars:
			vin_current_cars[car['reg']] = car
			vins_set.add(car['reg'])


	# Compare fetched data with current cars on file
	new_vehicle_count = 0
	email_subject = " near " + str(zipcode)
	email_content = """
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

	changed_vehicle_count = 0
	email_content_changed_vehicle = """
</ol>
<h3>Vehicle Information Changed:</h3>
<ol>
	"""
	for vehicle in vehicles_data:
		# If the vehicle informaion is on record, update the information
		vehicle_reg = vehicle['reg']
		if vehicle['reg'] in vin_current_cars.keys():
			is_changed = False
			vins_set.remove(vehicle_reg)
			for key in vehicle.keys():
				if vin_current_cars[vehicle_reg][key] != vehicle[key]:
					is_changed = True
				vin_current_cars[vehicle_reg][key] = vehicle[key]
			vehicle["record_date"] = vin_current_cars[vehicle_reg]["record_date"]
			if is_changed == True:
				changed_vehicle_count += 1
				email_content_changed_vehicle += generate_email_content(vehicle)
		# If not in, new car, set email and archive it
		else:	
			new_vehicle_count += 1
			vehicle["record_date"] = str(datetime.datetime.now()) 
			email_content += generate_email_content(vehicle)

	if changed_vehicle_count > 0:
		email_content += email_content_changed_vehicle

	email_content += """
	</ol>
	
	</body>
	</html>
	"""
	# Send an email to me for new E-Class:
	if new_vehicle_count > 0 or changed_vehicle_count > 0:
		if changed_vehicle_count > 0:
			email_subject = str(changed_vehicle_count) + " "+ class_name[class_number] +"-Class info changed"  + email_subject
		if new_vehicle_count > 0:
			email_subject = str(new_vehicle_count) + " new "+ class_name[class_number] +"-Class " + email_subject
		send_email(email_subject,email_content)

	# Update current car JSON file
	fout = open(working_directory+str(zipcode)+"_"+str(distance)+"_"+str(class_number)+'_current.json','w')
	fout.write(json.dumps(vehicles_data))
	fout.close()

	# Identify and update sold car file
	if len(vins_set) > 0:
		sold_cars = {}
		for vin in list(vins_set):
			vin_current_cars[vin]["sold_date"] = str(datetime.datetime.now())  
			sold_cars[vin] = vin_current_cars[vin]

		# Write to the archived JSON file
		fout = open(working_directory+str(zipcode)+"_"+str(distance)+"_"+str(class_number)+'_sold.json','a')
		fout.write(json.dumps(sold_cars.values()))
		fout.close()


def generate_email_content(vehicle):
	finance_rate = vehicle["apr"]
	dealer_name = vehicle["dln"]
	exterior = vehicle["ext"]
	interior = vehicle["int"]
	mileage = vehicle["mil"]
	phone_no = vehicle["phn"]
	ask_price= vehicle["pri"]
	vin = vehicle["reg"]
	year = vehicle["ryr"]
	drive = vehicle["vnt"]
	year_model = vehicle["ymo"]
	google_search_url = "http://www.google.com/search?q="+str(vin)
	carfax_url = "http://www.carfax.com/VehicleHistory/p/Report.cfx?vin="+str(vin)

	content = 	"""
	<li>
		<dl>
			<dt>Model: </dt><dd>
	"""
	content += str(year_model)
	content += """
			</dd>
			<dt>Drive: </dt><dd>
	"""
	content += str(drive)
	content += """
			</dd>
			<dt>Mileage: </dt><dd>
	"""
	content += str(mileage)
	content += """
			miles </dd>
			<dt>Price: </dt><dd>
	"""
	content += '$'+str(ask_price)
	content += """
			</dd>
			<dt>Dealer: </dt><dd>
	"""
	content += str(dealer_name)
	content += """
			</dd>
			<dt>Call: </dt><dd>
	"""
	content += str(phone_no)
	content += """
			</dd>
			<dt>Financing: </dt><dd>
	"""
	content += str(finance_rate)
	content += """
			%</dd>
			<dt>VIN: </dt><dd>
	"""
	content += str(vin)
	content += """
			</dd>
	"""
	content += '<dd><a href="http://www.google.com/search?q='+str(vin)+'">Google</a>\n'
	content += '<a href="http://www.carfax.com/VehicleHistory/p/Report.cfx?vin='+str(vin)+'">Carfax</a>'
	content += """
			</dd>
		</dl>
	</li>
	"""

	return content
