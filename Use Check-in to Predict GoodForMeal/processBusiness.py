# Command Line
# python processBusiness.py [input file path] [output file path] attr1 attr2 attr3
# e.g., python processBusiness.py business/Tempe_business.json output.csv business_id name BusinessParking
import json
import sys
import csv

args = sys.argv
input_file_path = args[1]
output_file_path = args[2]
attrs = args[3:]

attributes_direct = ['business_id','name','neighborhood','address','city','state','postal code','latitude','longitude','stars','review_count','is_open','categories','hours','attributes']
hasHours = False
attrs_notdirect = []
attrs_direct = []
if 'hours' in attrs:
	hasHours = true
for attr in attrs:
	if attr not in attributes_direct:
		attrs_notdirect.append(attr)
	else:
		attrs_direct.append(attr)

reload(sys)
sys.setdefaultencoding('utf-8')
file = open(input_file_path,'r')
with open(output_file_path,"wb") as csv_file:
	writer = csv.writer(csv_file, delimiter=",")
	writer.writerow(attrs_direct+attrs_notdirect)
	for line in file.readlines():
		entry = json.loads(line)
		output_row = []
		for attr in attrs_direct:
			output_row.append(entry[attr])
		if entry['attributes'] != None:
			for attr in attrs_notdirect:
				if attr in entry['attributes']:
					output_row.append(entry['attributes'][attr])
				else:
					output_row.append(None)
		writer.writerow(output_row)
