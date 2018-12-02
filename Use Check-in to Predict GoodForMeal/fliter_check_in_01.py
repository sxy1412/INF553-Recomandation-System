# fliter record with businessid in a set
# command line: python fliter_check_in.py [file of business_id] [output file]
import sys
import csv

args = sys.argv
neighbor = args[1].replace(" ","_")

id_file_input = args[1]
checkin_file_input = "checkin_las_vegas.csv"
checkin_file_output = args[2]

id_file = open(id_file_input,'r')
checkin_file = open(checkin_file_input,'r')
output_file = open(checkin_file_output,'wb')


business_id = []
for line in id_file:
	business_id.append(line.strip())

for line in checkin_file:
	tokens = line.split(",",2)
	if tokens[1] in business_id:
		output_file.write(tokens[1]+","+tokens[2])
output_file.close()
