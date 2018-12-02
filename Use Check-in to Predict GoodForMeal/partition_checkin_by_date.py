# command: python partition_checkin_by_date.py [Day] [Neighbor] [labeled/unlabeled]
# python partition_checkin_by_date.py Sun Downtown 0

import sys
import re
import csv

args = sys.argv
week = args[1]
neighbor = args[2].replace(" ","_")

input_file = open(neighbor+"_"+args[3]+"_checkin.csv","r")
output_file = open(neighbor+"_"+args[3]+"_checkin_" + week + ".csv","wb")
csv_reader = csv.reader(input_file, delimiter=',',quotechar='"')
csv_writer = csv.writer(output_file, delimiter=',')

header = ["business_id",0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
csv_writer.writerow(header)
for line in csv_reader:
	business_id = line[0]
	checkins = line[1][1:-1]
	checkins = checkins.replace("u\'","").replace("\'","")
	time_slots = checkins.split(", ")
	time24 = [0] * 24
	for slot in time_slots:
		if week in slot:
			tokens = slot.split("-")
			time, value = tokens[1].split(":")
			hour = int(time)
			time24[hour] = value
	csv_writer.writerow([business_id]+time24)
output_file.close()