import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
import json 

ratings_list = [i.strip().split("::") for i in open('ratings.dat', 'r').readlines()]
ratings_df = pd.DataFrame(ratings_list, columns = ['UserID', 'MovieID', 'Rating', 'Timestamp'], dtype = float)
#print(ratings_df)
R_df = ratings_df.pivot(index = 'UserID', columns ='MovieID', values = 'Rating').fillna(0)
R_df.head()
#print(R_df.head())
print(len(list(R_df.head())))
lists = []
for i in list(R_df.head()):
	lists.append(int(i))
json.dump(lists, open('MovieList.txt', 'w'))
R = R_df.as_matrix()
user_ratings_mean = np.mean(R, axis = 1)
R_demeaned = R - user_ratings_mean.reshape(-1, 1)


u, s, vt = svds(R_demeaned, k = 128)

sigma = np.diag(s)
vt = np.dot(sigma, vt)
print('Learning done')
df2 = pd.DataFrame(vt.T)
print(vt.T.shape)
df2.to_csv('Movie_Representation.csv')

