#command line: python get_businessid.py [neighbor]
#command line example: python get_businessid.py The\ Strip
import json
import sys
import csv

args = sys.argv
neighbor = args[1]
input_file = "LV_businesses_extracted.csv"
output_file_for_id = neighbor.replace(" ","_") + "_resturant_business_id.txt"
output_file = neighbor.replace(" ","_") + "_resturants_meal.csv"
output_file_id_GoodForMeal = neighbor.replace(" ","_") + "_labeled_business_id.txt"
output_file_GoodForMeal = neighbor.replace(" ","_") + "_labeled.csv"
output_file_unlabeled = neighbor.replace(" ","_") + "_unlabeled_business_id.txt"


# data =  open(input_file,'r')
output_for_id = open(output_file_for_id,'wb')
output = open(output_file,'wb')
output_GoodForMeal = open(output_file_GoodForMeal,'wb')
output_id_GoodForMeal = open(output_file_id_GoodForMeal,'wb')
output_unlabeled = open(output_file_unlabeled,'wb')

with open(input_file, 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=',',quotechar='"')
	writer_GoodForMeal = csv.writer(output_GoodForMeal, delimiter=',', quotechar='"')
	writer = csv.writer(output, delimiter=',', quotechar='"')
	for row in reader:
		if row[2] == neighbor and ("Restaurants" in row[3] or "Restaurants" in row[1]):
			output_for_id.write(row[0]+"\n")
			if len(row)>4:
				if row[4].strip() != "":
					GoodForMeal =  row[4].replace("{","").replace("}","")
					writer_GoodForMeal.writerow([row[0],GoodForMeal])
					output_id_GoodForMeal.write(row[0]+"\n")
				else:
					output_unlabeled.write(row[0]+"\n")
				writer.writerow([row[0],row[1],row[2],row[3],row[4]])
			else:
				writer.writerow([row[0],row[1],row[2],row[3]])
				output_unlabeled.write(row[0]+"\n")


output_for_id.close()
output.close()
output_GoodForMeal.close()
output_id_GoodForMeal.close()
output_unlabeled.close()

# for line in data:
# 	tokens = line.split(",",3)
# 	if tokens[2] == neighbor:
# 		output_for_id.write(tokens[0]+"\n")
# 		output.write(line)
# output_for_id.close()
# output.close()
