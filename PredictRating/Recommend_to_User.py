import pandas as pd
import numpy as np
import timeit
from predict_rating import Predict_Rating

start = timeit.default_timer()

def Recommend(  User_ID,
                Time,
                Path_Business_List,
                Path_review_rating,
                Path_other_users_list,
                Path_business_similarity_matrix,
                Path_Result  ):

    Business_List = pd.read_csv(Path_Business_List, header=0, parse_dates=True) #(business_id, breakfast, lunch, dinner)
    Review_Rating_df = pd.read_csv(Path_review_rating, header=0, parse_dates=True) #(user_id, business_id, rating)
    Business_similarity_matrix_df = pd.read_csv(Path_business_similarity_matrix, header=0, index_col=0, parse_dates=True)

    UserID_been_to = Review_Rating_df.loc[Review_Rating_df['user_id'] == User_ID] #(user_id, business_id, rating)

    #print("All business : {}".format(len(Business_List.index)))

    print("User been to : {}".format(len(UserID_been_to.index)))

    UserID_NOT_been_to = UserID_been_to['business_id'].append(Business_List['business_id']).drop_duplicates(keep=False)
    print("User not been to : {}".format(len(UserID_NOT_been_to.index)))

    numberOfRows = UserID_NOT_been_to.size

    User_Business_Predict = pd.DataFrame(index=np.arange(0, numberOfRows), columns=['user_id', 'business_id', 'rating'])

    count = 0
    for row in UserID_NOT_been_to:
        print(count)
        start = timeit.default_timer()

        temp = Predict_Rating(User_ID, row, Path_other_users_list, Review_Rating_df, Business_similarity_matrix_df, Path_review_rating)

        print(temp)

        stop = timeit.default_timer()
        print('Time: ', stop - start)

        User_Business_Predict.loc[count]['user_id'] = temp[0]
        User_Business_Predict.loc[count]['business_id'] = temp[1]
        User_Business_Predict.loc[count]['rating'] = temp[2]

        count = count + 1

    User_Business_Predict_Sorted = User_Business_Predict.sort_values(User_Business_Predict.columns[2],ascending = False).loc[User_Business_Predict['rating'] > 3.5]

    print(User_Business_Predict_Sorted)

    User_Business_Predict_Sorted.to_csv(Path_Result, index = False)


#INPUTS=========================================================================
User_ID = "qQecSd0lynfB4g-LPa9JCw"
Time = "lunch"
Path_Strip_Business_List = "strip_GoodForMeal.csv"
Path_Strip_review_rating = "strip_ratings_train_qQecSd0lynfB4g-LPa9JCw.txt"
Path_other_users_list = "business_userslist.txt"
Path_business_similarity_matrix =  "strip_business_similarity.csv"
Path_Result = "{}_Predicted_Result.csv".format(User_ID)
#===============================================================================

Recommend(User_ID, Time, Path_Strip_Business_List, Path_Strip_review_rating, Path_other_users_list, Path_business_similarity_matrix, Path_Result)

stop = timeit.default_timer()
print('Total Time: ', stop - start)
