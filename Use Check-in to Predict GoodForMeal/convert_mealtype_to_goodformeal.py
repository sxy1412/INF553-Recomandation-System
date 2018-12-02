import sys
import csv
args = sys.argv
inputfile = open(args[1],"r")
outputfile = open(args[1]+"_GoodForMeal.csv","wb")
reader = csv.reader(inputfile, delimiter=',',quotechar='"')
writer = csv.writer(outputfile, delimiter=',', quotechar='"')
header = ["business_id","breakfast","lunch","dinner"]
writer.writerow(header)
for row in reader:
	business_id = row[0]
	mealtype = row[1]
	if mealtype == '0':
		writer.writerow([business_id,"FALSE","FALSE","FALSE"])
	if mealtype == '1':
		writer.writerow([business_id,"FALSE","FALSE","TRUE"])
	if mealtype == '10':
		writer.writerow([business_id,"FALSE","TRUE","FALSE"])
	if mealtype == '11':
		writer.writerow([business_id,"FALSE","TRUE","TRUE"])
	if mealtype == '100':
		writer.writerow([business_id,"TRUE","FALSE","FALSE"])
	if mealtype == '101':
		writer.writerow([business_id,"TRUE","FALSE","TRUE"])
	if mealtype == '110':
		writer.writerow([business_id,"TRUE","TRUE","FALSE"])
	if mealtype == '111':
		writer.writerow([business_id,"TRUE","TRUE","TRUE"])

outputfile.close()