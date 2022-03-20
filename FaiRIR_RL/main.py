from iFair import iFair
import numpy as np
import json
import csv
import pandas as pd
from sklearn.preprocessing import normalize

def main():
	Movie_Representation = {}
	Movies = json.load(open('MovieList.txt', 'r'))
	#print(type(Movies[0]))
	#exit(0)
	count = 0
	with open('Movie_Representation.csv', 'r') as CSV_file:
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
	dfair.to_csv('svdFair.csv')

if __name__ == '__main__':
	main()
