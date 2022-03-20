import pandas as pd
import json 
import csv
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

Movie_Representation = {}
with open('Movies.emb', 'r') as fh:
	for line in fh:
		if len (line.split(' ')) <= 2:
			print(line.split(' '))
		#Movies.append(row[0])
		else:
			mov = int(line.split(' ')[0])
			embed = line.split(' ')[1:]
			embed = [float(i) for i in embed]
			Movie_Representation[mov] = embed
			

print(len(Movie_Representation.keys()))

Movies = json.load(open('MovieList.txt', 'r'))
print(Movies[:10])

Embeddings = []
Nodes = []
for node in Movies:
	Embeddings.append(Movie_Representation[node])
	Nodes.append(node)

Embeddings = np.array(Embeddings)
'''
B = np.array(Embeddings)
print(B.shape)
C = pd.read_csv('RatingSimI2V.csv', index_col = 0 )
D = np.array(C)
Embeddings = np.matmul(D, B)
'''
Embeddings = normalize(Embeddings)
SIM = cosine_similarity(Embeddings, dense_output = True)
SIMdf = pd.DataFrame(SIM, columns = Movies)
SIMdf.to_csv('SimilarityI2V.csv')
