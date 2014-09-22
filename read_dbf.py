#! /usr/bin/python

from dbfpy import dbf

fout = open("/users/chhuang/Desktop/Car/vehicle_accident_report.txt","w")
fout.write("Year\tMake\tMode\tMake_Code\tMode_code\tMode_year\n")

for year in range(2010,2013):
	print str(year)+": "
	count = 0
	db = dbf.Dbf("/users/chhuang/Desktop/Car/FARS"+str(year)+"/person.DBF")
	for rec in db:
		# Get the list of cars that causes fatal death:
		count += 1
		print "\t"+str(count)
		if rec["INJ_SEV"] == 4:
			# Year+Make + Mode + Make(Code) + Mode(Code) + Car_Year 
			fout.write(str(year)+"\t"+rec["VINMAKE"]+"\t"+rec["VINA_MOD"]+"\t"+str(rec["MAKE"])+"\t"+str(rec["MAK_MOD"])+"\t"+str(rec["MOD_YEAR"])+"\n")

print "Finished"
fout.close()