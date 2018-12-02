import pandas as pd
import sys

f=open(sys.argv[1],'r')
dict={}

for line in f.readlines():

    t=line.split(",",1)
    dict[t[0]]=t[1][4:len(t[1])-1].split(", ")


threshold=float(sys.argv[2])

df=pd.read_csv(sys.argv[0])
recommand_list=df[df.rating>=threshold]["business_id"].tolist()
user=df.loc[1,"user_id"]
true_list=[]
false_list=[]
for business in recommand_list:
    if user in dict[business]:
        true_list.append(business)
    else:
        false_list.append(business)
outf=open("result.txt",'w')

outf.write("True results:\n")
for business in true_list:
    outf.write(business+"\n")

outf.write("False results:\n")
for business in false_list:
    outf.write(business+"\n")

outf.close()
