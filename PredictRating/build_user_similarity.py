
def Build_user_similarity(user_id, user_list_path, rating_path):
    import pandas as pd
    import math

    def find_similarity(user):
        #rtn={}
        userlist=[]
        simlist=[]
        count=0
        for other_user in users:
            count+=1
            #print(count)
            if user==other_user:

                continue
            restaurants1=df.loc[df.user_id==user,"business_id"].values.tolist()
            restaurants2=df.loc[df.user_id==other_user,"business_id"].values.tolist()
            restaurants=set(restaurants1) & set(restaurants2)
            mean1=df.loc[df.user_id==user,"rating"].mean()
            mean2=df.loc[df.user_id==other_user,"rating"].mean()
            up=0.0
            down1=0.0
            down2=0.0
            for rest in restaurants:
                up+=(rating[(user,rest)]-mean1)*(rating[(other_user,rest)]-mean2)
                down1+=pow(rating[(user,rest)]-mean1,2)
                down2+=pow(rating[(other_user,rest)]-mean1,2)
            #rtn[other_user]=up/(math.sqrt(down1)*math.sqrt(down2))
            userlist.append(other_user)
            if down1*down2==0:
                simlist.append(0)
            else:
                simlist.append(up/(math.sqrt(down1)*math.sqrt(down2)))
        return pd.DataFrame({"user_id":userlist,"similarity":simlist})


    df=pd.read_csv(rating_path)
    users_f=open(user_list_path,'r')
    users=set()
    for line in users_f.readlines():
        users.add(line[:-1])

    rating={}

    for i in df.index:
        rating[(df.loc[i,"user_id"],df.loc[i,"business_id"])]=df.loc[i,"rating"]

    return find_similarity(user_id)
