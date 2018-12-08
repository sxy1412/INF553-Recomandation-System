# Input: Single business_id
# Output: List of simialr business ids

import pandas as pd
import numpy as np

def Get_similar_business(business_id, similarity_threshold, Business_similarity_matrix):
    #Business_similarity_matrix = pd.read_csv(matrix_path, header=0, index_col=0, parse_dates=True)
    if (business_id in Business_similarity_matrix.index):
        All_similarity = Business_similarity_matrix.loc[business_id]
        Simialr_Business = All_similarity[All_similarity >= similarity_threshold].index.to_frame()
        return Simialr_Business
    else:
        return pd.DataFrame(columns=['business_id'])


    #Simialr_Business.to_csv(output_path,
    #                        sep='\t',
    #                        index=False,
    #                        header = False)

    #return Simialr_Business

#===============================================================================
# inputs
#Business_ID = "kgffcoxT6BQp-gJ-UQ7Czw"
#Similarity_Threshold = 0.5
#business_similarity_matrix_path = "C:/Users/Sandie/Desktop/Fall2018/INF553/Project/Data/Business_similarity/Strip_similarity.csv"
#output_path = "C:/Users/Sandie/Desktop/Fall2018/INF553/Project/Data/Business_similarity/Similarity_output.csv"
#===============================================================================

#Simialr_Business = get_similar_business(Business_ID, Similarity_Threshold, business_similarity_matrix_path)
#print(Simialr_Business)

#np.savetxt(r'C:\Users\Sandie\Desktop\Fall2018\INF553\Project\Temp_Data\similar_business.txt', Simialr_Business.values, fmt='%d')
#Simialr_Business.to_csv(r'C:\Users\Sandie\Desktop\Fall2018\INF553\Project\Temp_Data\similar_business.txt', header=None, index=None, sep=' ', mode='a')
