#command line: python mealtype_csv.py [neighbor]
import sys
import csv
args = sys.argv
neighbor = args[1].replace(" ","_")
output_file = open(neighbor+"_mealtype.csv","wb")
output_file_labeled = open(neighbor+"_mealtype_labeled.csv","wb")
with open(neighbor+"_labeled.csv", "r") as inputfile:
	reader = csv.reader(inputfile, delimiter=',',quotechar='"')
	writer = csv.writer(output_file, delimiter=',', quotechar='"')
	writer_labeled = csv.writer(output_file_labeled, delimiter=',', quotechar='"')
	writer.writerow(["business_id","breakfast","lunch","dinner","mealtype_label"])
	writer_labeled.writerow(["business_id","breakfast","lunch","dinner"])
	for row in reader:
		business_id = [row[0]]
		mealtype = []
		category = 0
		if "\'breakfast\': True" in row[1]:
			mealtype.append(True)
			category += 1
		else:
			mealtype.append(False)
		if "\'lunch\': True" in row[1]:
			mealtype.append(True)
			category =  category*10 + 1
		else:
			mealtype.append(False)
			category *= 10
		if "\'dinner\': True" in row[1]:
			mealtype.append(True)
			category =  category*10 + 1
		else:
			mealtype.append(False)
			category *= 10
		# if "\'brunch\': True" in row[1]:
		# 	mealtype.append(True)
		# 	# category =  category*10 + 1
		# else:
		# 	mealtype.append(False)
		# 	# category *= 10
		# if "\'latenight\': True" in row[1]:
		# 	mealtype.append(True)
		# 	# category =  category*10 + 1
		# else:
		# 	mealtype.append(False)
		# 	# category *= 10
		writer_labeled.writerow(business_id+mealtype)
		mealtype.append(category)
		writer.writerow(business_id+mealtype)
output_file_labeled.close()
output_file.close()