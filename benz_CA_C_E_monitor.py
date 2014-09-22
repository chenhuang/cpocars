#! /usr/bin/python

import benz_cpo_monitor

zipcode = 95101
distance = 50
class_number = 3

# E-Class
year_from = 2010
year_to = 2013
data = benz_cpo_monitor.fetch_data(zipcode, distance, class_number, year_from, year_to)
benz_cpo_monitor.update(data, zipcode, distance, class_number)

# C-Class
class_number = 2
year_from = 2011
year_to = 2011
data = benz_cpo_monitor.fetch_data(zipcode, distance, class_number, year_from, year_to)
benz_cpo_monitor.update(data,zipcode,distance,class_number)

