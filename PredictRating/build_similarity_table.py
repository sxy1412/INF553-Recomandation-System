import pandas as pd
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

df=pd.read_csv("Summerlin_resturants_meal.csv")
category={}
business_id=[]
for i in df.index:
    business_id.append(df.loc[i,"business_id"])
    df.loc[i,"categories"]
    category[df.loc[i,"business_id"]]=set(str(df.loc[i,"categories"]).split(', '))

df1=pd.DataFrame([[0 for _ in xrange(len(business_id))] for __ in xrange(len(business_id))],index=business_id,columns=business_id)

count=0
for i in df1.index:
    count+=1
    print count
    for j in df1.columns:
        df1.loc[i,j]=float(len(category[i] & category[j]))/float(len(category[i] | category[j]))

df1.to_csv("similarity.csv")

