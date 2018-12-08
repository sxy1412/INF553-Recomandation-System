#inputs:    1. (UserID, BusinessID)
#           2. 2 List of supporting users (UserID, weight), One direct, One indirect
#           3. Review_Rating.csv?
# Assume
# Review_Rating Format: (UserID, BusinessID, Rating)

import pandas as pd
import numpy as np
import timeit
from build_user_similarity import Build_user_similarity
from get_similar_business import Get_similar_business

def Predict_Rating( UserID,
                    BusinessID,
                    Path_other_users_list,
                    Review_rating_df,
                    business_similarity_matrix_df,
                    Path_review_rating):

    def Get_user_avg_rating(Uid):
        User_ratings = (Review_rating_df.loc[Review_rating_df['user_id'] == Uid])['rating']

        if (User_ratings.size == 0):
            # If user not rated anything
            return 3

        User_rating_avg = float(sum(User_ratings)) / User_ratings.size
        return User_rating_avg

    def Get_business_avg_rating(Bid):
        Business_ratings = (Review_rating_df.loc[Review_rating_df['business_id'] == Bid])['rating']

        if (Business_ratings.size == 0):
            # If business does not have any ratings
            return 3

        Business_rating_avg = float(sum(Business_ratings)) / Business_ratings.size
        return Business_rating_avg

    #User_avg
    UserA_rating_avg = Get_user_avg_rating(UserID)
    Business_rating_avg = Get_business_avg_rating(BusinessID)

    # DIRECT USERS==================================================================
    #Users been to Business
    Users_been_to_Business = Review_rating_df.loc[Review_rating_df['business_id'] == BusinessID]
    if (Users_been_to_Business.size == 0):
        return (UserID, BusinessID, UserA_rating_avg)

    Users_been_to_Business['user_id'].to_csv(Path_other_users_list, header=None, index=None, mode='w') #(user_id,business_id,rating)
    #print("[Direct] Number of users been to business : {}".format(len(Users_been_to_Business.index)))

    if (len(Users_been_to_Business.index) > 400):
        #print("[Direct] Number of users been to business : {}".format(len(Users_been_to_Business.index)))
        return (UserID, BusinessID, (UserA_rating_avg/5)*Business_rating_avg)

    #User similarity of people been to business
    #print("============================================")
    Other_User_Similarity = Build_user_similarity(UserID, Path_other_users_list, Path_review_rating) #(user_id, similarity)
    #print("============================================")
    UserA_Similarity = pd.merge(Users_been_to_Business,Other_User_Similarity, on=['user_id'])
    UserA_Similarity = UserA_Similarity[UserA_Similarity['similarity'] > 0.5].sort_values(by=['similarity'], ascending=False) #(user_id, business_id, rating, similarity)
    #print("[Direct] Number of similar users : {}".format(len(UserA_Similarity.index)))

    # if no user is similar
    if (UserA_Similarity.empty == True):
        return (UserID, BusinessID, UserA_rating_avg)

    #Find other users average rating
    UserA_Similarity['user_avg'] = UserA_Similarity.apply (lambda row: Get_user_avg_rating(row['user_id']),axis=1) #(user_id, business_id, rating, similarity, user_avg)

    Top = sum(UserA_Similarity.apply (lambda row:(row['rating']-row['user_avg'])*(row['similarity']),axis=1))
    Bottom = sum(UserA_Similarity['similarity'])

    Direct_prediction = UserA_rating_avg + Top/Bottom

    #INDIRECT USERS=================================================================

    #get similar business
    Simialr_Business = Get_similar_business(BusinessID, 0.5, business_similarity_matrix_df)
    if (Simialr_Business.empty):
        return (UserID, BusinessID, Direct_prediction)

    Top_Similar_Business = str(Simialr_Business.iloc[0,0])
    #print("[Indirect] Top similar businessID : {}".format(Top_Similar_Business))

    #Users been to Similar_Business
    Users_been_to_Business = Review_rating_df.loc[Review_rating_df['business_id'] == Top_Similar_Business]
    if (Users_been_to_Business.size == 0):
        return (UserID, BusinessID, Direct_prediction)

    Users_been_to_Business['user_id'].to_csv(Path_other_users_list, header=None, index=None, mode='w') #(user_id,business_id,rating)
    #print("[Indirect] Number of users been to business : {}".format(len(Users_been_to_Business.index)))

    if (len(Users_been_to_Business.index) > 400):
        #print("[Direct] Number of users been to business : {}".format(len(Users_been_to_Business.index)))
        return (UserID, BusinessID, Direct_prediction )

    #User similarity of people been to business
    #print("============================================")
    Other_User_Similarity = Build_user_similarity(UserID, Path_other_users_list, Path_review_rating) #(user_id, similarity)
    #print("============================================")
    UserA_Similarity = pd.merge(Users_been_to_Business,Other_User_Similarity, on=['user_id'])
    UserA_Similarity = UserA_Similarity[UserA_Similarity['similarity'] > 0.3].sort_values(by=['similarity'], ascending=False) #(user_id, business_id, rating, similarity)
    #print("[Indirect] Number of similar users : {}".format(len(UserA_Similarity.index)))


    # if no user is similar
    if (UserA_Similarity.empty == True):
        return (UserID, BusinessID, Direct_prediction)

    #Find other users average rating
    UserA_Similarity['user_avg'] = UserA_Similarity.apply (lambda row: Get_user_avg_rating(row['user_id']),axis=1) #(user_id, business_id, rating, similarity, user_avg)

    Indirect_Top = sum(UserA_Similarity.apply (lambda row:(row['rating']-row['user_avg'])*(row['similarity']),axis=1)) * 0.7
    Indirect_Bottom = sum(UserA_Similarity['similarity'])*0.7

    return (UserID, BusinessID, UserA_rating_avg + ((Top + Indirect_Top)/(Bottom + Indirect_Bottom)))

""" Testing
# input ========================================================================
Path_review_rating = "C:/Users/Sandie/Desktop/Fall2018/INF553/Project/Data/strip_ratings.csv"
Path_other_users_list = "C:/Users/Sandie/Desktop/Fall2018/INF553/Project/Temp_Data/business_userslist.txt"
Path_business_similarity_matrix = "C:/Users/Sandie/Desktop/Fall2018/INF553/Project/Data/strip_business_similarity.csv"
user_id = "AuIK5tF2GjO7SftHawTLKw"
business_id = "8Q6jl7OW8DZzwANggDspcw"
#===============================================================================

Review_Rating_df = pd.read_csv(Path_review_rating, header=0, parse_dates=True)

Result = Predict_Rating(user_id, business_id, Path_other_users_list, Review_Rating_df, Path_business_similarity_matrix)
print(Result)
"""
