import pandas as pd

f=open('strip_business_user_dict.txt','r')
dict={}

for line in f.readlines():

    t=line.split(",",1)
    dict[t[0]]=t[1][4:len(t[1])-1].split(", ")


threshold=3.5 #can be changed to command line argument

df=pd.read_csv("qQecSd0lynfB4g-LPa9JCw_Predicted_Result.csv")
recommand_list=df[df.rating>threshold]["business_id"].tolist()
user=df.loc[1,"user_id"]
true_list=[]
false_list=[]
for business in recommand_list:
    if user in dict[business]:
        true_list.append(business)
    else:
        false_list.append(business)
outf=open("qQecSd0lynfB4g-LPa9JCw_result.txt",'w')

outf.write("True results:\n")
for business in true_list:
    outf.write(business+"\n")

outf.write("False results:\n")
for business in false_list:
    outf.write(business+"\n")

outf.write("Ratio:\nNumber of restaurants user visited " + str(len(true_list)) + " / Total number of restaurants recommended " + str(len(true_list) + len(false_list) ))


outf.close()
