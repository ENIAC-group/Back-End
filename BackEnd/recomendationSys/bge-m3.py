from FlagEmbedding import BGEM3FlagModel
import numpy as np
# Setting use_fp16 to True speeds up computation with a slight performance degradation

model = BGEM3FlagModel('BAAI/bge-m3',  
                       use_fp16=True) 
def getting_similarities( user_info , doctors_list ) : 
    if len ( doctors_list ) == 0 : 
        return []
    if not user_info : 
        return []
    embeddings_1 = model.encode(user_info, 
                            batch_size=12, 
                            max_length=300, # If you don't need such a long length, you can set a smaller value to speed up the encoding process.
                            )['dense_vecs']
    embeddings_2 = model.encode(doctors_list)['dense_vecs']
    similarity = embeddings_1 @ embeddings_2.T

    return sorted(np.sort(similarity[0])[::-1] )
    

# model = BGEM3FlagModel('BAAI/bge-m3',  
#                        use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation
# s1 = "جنسیت : زن"
# s1 += "\nبیماری افسردگی در خانواده من ارثی است. من دوره درمان اضطراب را گذرانده ام . "

# sentences_1 = [s1]
# sentences_2 = [". من دکتر عبدی هستم. در زمینه بیماری های روان شناختی افسردگی کار میکنم .نظرم بر این است که این بیماری های ارئی هستند "  , "دکتر علی زاده . اکثر بیمار های ارثی ترجیج میدهم خانوم باشند "
#                ". من دکتر عبدی هستم. در زمینه بیماری های روان شناختی افسردگی کار میکنم .نظرم بر این است که این بیماری های ارئی هستند " , ". من دکتر عبدی هستم. در زمینه بیماری های روان شناختی افسردگی کار میکنم .نظرم بر این است که این بیماری های ارئی هستند "
#                ". من دکتر عبدی هستم. در زمینه بیماری های روان شناختی افسردگی کار میکنم .نظرم بر این است که این بیماری های ارئی هستند " , ". من دکتر عبدی هستم. در زمینه بیماری های روان شناختی افسردگی کار میکنم .نظرم بر این است که این بیماری های ارئی هستند "
#                ". من دکتر عبدی هستم. در زمینه بیماری های روان شناختی افسردگی کار میکنم .نظرم بر این است که این بیماری های ارئی هستند " , ". من دکتر عبدی هستم. در زمینه بیماری های روان شناختی افسردگی کار میکنم .نظرم بر این است که این بیماری های ارئی هستند " 
#                ". من دکتر عبدی هستم. در زمینه بیماری های روان شناختی افسردگی کار میکنم .نظرم بر این است که این بیماری های ارئی هستند " , ". من دکتر عبدی هستم. در زمینه بیماری های روان شناختی افسردگی کار میکنم .نظرم بر این است که این بیماری های ارئی هستند "]

# embeddings_1 = model.encode(sentences_1, 
#                             batch_size=12, 
#                             max_length=300, # If you don't need such a long length, you can set a smaller value to speed up the encoding process.
#                             )['dense_vecs']
# embeddings_2 = model.encode(sentences_2)['dense_vecs']
# similarity = embeddings_1 @ embeddings_2.T
# print(np.sort(similarity[0])[::-1])
