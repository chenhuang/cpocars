#! /usr/bin/python
# Read www.mypreownedmercedes.com/used and load latest E-Class cars
# NOTE: This script does not work, the working way is to do GET request on http://www.mypreownedmercedes.com/mbucl?search={%22country2%22:%22US%22,%22hits%22:{%22to%22:999},%22cpo%22:1,%22postcode%22:%2220770%22,%22distance%22:{%22to%22:%2250%22},%22year%22:{%22to%22:9998},%22order%22:[%22pricea%22],%22class_bodystyle%22:[{%22class%22:3,%22bodystyle%22:[1],%22model%22:[],%22variant%22:[]}]}

import os
import sys
import re
import urllib2, urllib

values = {}
#values['locatorcondition'] = '{"postcode":"20770","distance":"50","viewtype":"cpo","pricemin":0,"pricemax":0,"mileagemin":"any","engine":"any","transmission":"any","colour":"","yearmin":"2011","yearmax":"any","matrix":[{"classinfo":3,"bodystyle":1,"model":["2967"],"variant":[],"order":1}],"showsaved":false,"feature":[],"amg":false,"pageitem":96,"listtype":"list","viewpagenumber":0,"advancedopened":false,"deeplink_class":"","directors":"false","orderby":"pricea"}'
#values['locatorcondition'] = '{"postcode":"20770","distance":"50","viewtype":"cpo"}'
values['locatorcondition'] = '{"postcode":"20770","distance":"50","viewtype":"cpo"}'
values['postcode'] = "20770"
values['distance'] = "50"
values['viewtype'] = 'cpo'
print values
#params = urllib.urlencode({'@postcode':'20770','@distance':'50','@viewtype':'CPO','@yearmin':'2011', '@classinfo':'3', '@bodystyle':'1', '@order':'1','@pageitem':'96','@listtype':'list','@orderby':'pricea'})
#params = urllib.urlencode({'locatorcondition':'{"postcode":"20770","distance":"50","viewtype":"cpo","pricemin":0,"pricemax":0,"mileagemin":"any","engine":"any","transmission":"any","colour":"","yearmin":"2011","yearmax":"any","matrix":[{"classinfo":3,"bodystyle":1,"model":["2967"],"variant":[],"order":1}],"showsaved":false,"feature":[],"amg":false,"pageitem":96,"listtype":"list","viewpagenumber":0,"advancedopened":false,"deeplink_class":"","directors":"false","orderby":"pricea"}'})

data = urllib.urlencode(values)
req = urllib2.Request('http://www.mypreownedmercedes.com/used',data)
response = urllib2.urlopen(req)
the_page = response.read()

fout=open("./t.html","w")
fout.write(the_page)
fout.close()
print "Done"
