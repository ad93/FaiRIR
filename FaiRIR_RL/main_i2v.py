from iFair import iFair
import numpy as np
import json
import csv
import pandas as pd
from sklearn.preprocessing import normalize

def main():
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
	Embeddings = normalize(Embeddings)
	I_FAIR = iFair()
	Fair_Embeddings = I_FAIR.fit_transform(Embeddings)
	dfair = pd.DataFrame(Fair_Embeddings)#, columns= ['a', 'b', 'c', 'd', 'e'])
	dfair.to_csv('i2vFair.csv')

if __name__ == '__main__':
	main()
