import networkx as nx
import numpy as np
import json
import math
import csv
import operator
import pandas as pd
from tqdm import tqdm

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% All IMPORTS DONE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Similarity = pd.read_csv('FairSimilaritySVD.csv')
#with open ('DeservedExposure.json', 'r') as fp:
#	initial = json.load(fp)
#KEYS = list(initial.keys())
#CANDIDATES = list(Similarity.head())[1:]

ITEMS = list(Similarity.head())[1:]
print(len(ITEMS))
#exit(0)
RatingInfo = {}
with open('RatingInfo.csv', 'r') as csv_file:
	reader = csv.reader(csv_file)
	for row in reader:
		if row[0] == '':
			continue
		RatingInfo [row[0]] = float(row[1])
#exit(0) 
k = 25
Recommendations = {}

'''Movies = []
with open('RatingInfo.csv', 'r') as csv_file:
	reader = csv.reader(csv_file)
	for row in reader:
		if row[0] == '':
			continue
		Movies.append(row[0])
print(len(Movies))'''

def Select_Neighbors(item, k):
	Node_Similarities = {}
	ind = ITEMS.index(item)
	for neighbor in ITEMS:
		Node_Similarities[neighbor] = Similarity.loc[ind, neighbor] #* (1 / math.exp (abs(RatingInfo[item]-RatingInfo[neighbor])))
	sorted_similarity = sorted(list(Node_Similarities.items()), key=operator.itemgetter(1), reverse = True)
	Neighbors = []
	#print(sorted_similarity[:20])
	for element in sorted_similarity[1:26]:
		Neighbors.append(element[0])
	return list(Neighbors)

def main():
	with tqdm(total=len(ITEMS)) as pbar:
		for item in ITEMS:
			#print(item)
			Neighbors = Select_Neighbors(item, k)
			Recommendations[item] = Neighbors
			pbar.update(1)
			#exit(0)
	#print(Recommendations)
	json.dump(Recommendations, open('Phase1Recommendation_SVD.json', 'w'))

if __name__== '__main__':
	main()
