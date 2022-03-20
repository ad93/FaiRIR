#import sklearn.metrics.pairwise as pairwise
import pandas as pd
import json 
import csv
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

count = 0
Movie_Representation = {}
Movies = json.load(open('MovieList.txt', 'r'))
#print(type(Movies[0]))
#print(len(Movies))
#exit(0)
with open('./representation/svdFair.csv', 'r') as CSV_file:
	reader = csv.reader(CSV_file)
	for row in reader:
		if row[0] == '':
			#print(row)
			continue
		#print(row)
		embed = row[1:]
		embed=[float(i) for i in embed]
		Movie_Representation[Movies[count]] = embed
		count += 1

print(len(Movie_Representation.keys()))
#print(len(Movie_Representation[1]))


Embeddings = []
Nodes = []
for node in Movies:
	Embeddings.append(Movie_Representation[node])
	Nodes.append(node)

Embeddings = np.array(Embeddings)
Embeddings = normalize(Embeddings)
SIM = cosine_similarity(Embeddings, dense_output = True)
SIMdf = pd.DataFrame(SIM, columns = Movies)
SIMdf.to_csv('FairSimilaritySVD.csv')
