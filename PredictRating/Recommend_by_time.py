import pandas as pd
import numpy as np

def Recommend_by_time(Path_rec_list,Path_Business_List, time):
    Rec_bussiness_list = pd.read_csv(Path_rec_list, header=0, parse_dates=True) #(user_id, business_id, rating)
    #Rec_bussiness_list = Rec_bussiness_list['business_id']

    print(Rec_bussiness_list)

    Business_List = pd.read_csv(Path_Business_List, header=0, parse_dates=True) #(business_id, breakfast, lunch, dinner)

    print(Business_List)

    A = pd.merge(Rec_bussiness_list,Business_List, on=['business_id'])

    A = A.loc[A[time] == True]

    return (A)


Path_rec_list = "C:/Users/Sandie/Desktop/Fall2018/INF553/Project/Results/qQecSd0lynfB4g-LPa9JCw_Predicted_Result.csv"
Path_Strip_Business_List = "C:/Users/Sandie/Desktop/Fall2018/INF553/Project/Data/strip_GoodForMeal.csv"
time = 'lunch'

B = Recommend_by_time(Path_rec_list, Path_Strip_Business_List, time)


Path_Result = "C:/Users/Sandie/Desktop/Fall2018/INF553/Project/Results/qQecSd0lynfB4g-LPa9JCw_{}_Predicted_Result.csv".format(time)
B.to_csv(Path_Result, index = False)

print(B)
