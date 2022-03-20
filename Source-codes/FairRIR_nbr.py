import networkx as nx
import numpy as np
import json
import math
import csv
import operator
import pandas as pd
from tqdm import tqdm
import scipy.stats as ss

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% All IMPORTS DONE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Similarity = pd.read_csv('SimilaritySVD.csv')
with open ('DeservedExposure.json', 'r') as fp:
	initial = json.load(fp)
B = []
BM = []
Deserved = {}
Count = {}
for key in sorted(list(initial.keys())):
	Deserved[key] = int(math.floor(initial[key] * 10677 * 10))
	Count[key] = 0
A = sorted(list(Deserved.items()), key=operator.itemgetter(1), reverse = True)

print(sum(list(Deserved.values())))
for element in A:
	B.append(element[0])
	BM.append(element[0])
	if sum(list(Deserved.values())) < 106770:
		Deserved[element[0]] += 1
print(sum(list(Deserved.values())))
#exit(0)
Below_Minimums = BM
ITEMS = list(Similarity.head())[1:]
print(ITEMS[:10])
print(len(ITEMS))

Recommendations = {}


def Upgrade(Neighbors, Below_Minimums):
	for element in Neighbors:
		Count[element] += 1
		if Count[element] == Deserved[element]:
			Below_Minimums.remove(element)
	#return Below_Minimums

def Select_Neighbors(item, k, Lists):
	Node_Similarities = []
	Deservingness = []
	ind = ITEMS.index(item)
	for neighbor in Lists:
		Node_Similarities.append(Similarity.loc[ind, neighbor])
		Deservingness.append(Deserved[neighbor]-Count[neighbor])
	Similarity_Rank = ss.rankdata(Node_Similarities)
	Deserving_Rank = ss.rankdata(Deservingness)
	Node_Rank = {}
	for i in range(len(Lists)):
		Node_Rank[Lists[i]] = (Similarity_Rank[i] + Deserving_Rank[i])/2.0
	sorted_similarity = sorted(list(Node_Rank.items()), key=operator.itemgetter(1), reverse = True)
	Neighbors = set()
	#print(sorted_similarity[:10])
	#exit(0)
	for element in sorted_similarity:
		if element[0] == item:
			continue
		elif len(Neighbors) == k:
			break
		else:
			Neighbors.add(element[0])
	
	return list(Neighbors)

def main():
	print(len(B))
	#exit(0)
	with tqdm(total=len(ITEMS)) as pbar:
		for item in B:
			Neighbors = Select_Neighbors(item, 10, Below_Minimums)
			Upgrade(Neighbors, Below_Minimums) 
			Recommendations[item] = Neighbors
			pbar.update(1)
			
	print(len(Below_Minimums))
	json.dump(Recommendations, open('FairRecommendation_SVD.json', 'w'))

if __name__== '__main__':
	main()
