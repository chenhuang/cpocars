import volvo_cpo_monitor

zipcode = 95101
distance = 50
class_number = 'S80'
year_from = 2011
year_to = 2014

data = volvo_cpo_monitor.fetch_data(zipcode,distance,class_number,year_from,year_to)
volvo_cpo_monitor.update(data, zipcode, distance, class_number)

