import json
import networkx as nx
import csv
import operator
import math
from tqdm import tqdm 
from scipy.stats import entropy

Recommendations = json.load(open('Phase1Recommendation_I2V.json', 'r'))
print(len(Recommendations.keys()))
#exit(0)
G = nx.DiGraph()
k = 10
RatingInfo = {}
Movies = {}
with open('movies.dat', 'r') as csv_file:
	reader = csv_file.readlines()
	for row in reader:
		row = row.strip().split("::")
		if row[0] == 'movieId':
			continue
		Movies[row[0]] = row[1]

Popularity = {}
PopularityExp = {}
with open('RatingInfo.csv', 'r') as csv_file:
	reader = csv.reader(csv_file)
	for row in reader:
		if row[0]=='':
			continue
		Popularity[row[0]] = float(row[2])	

sum_of_popularity = sum(Popularity.values())
num_of_movies = len(Popularity.values())

for key in Popularity:
	PopularityExp[key] = Popularity[key]/sum_of_popularity
print(sum(PopularityExp.values()))
print(num_of_movies)
#exit(0)		
def divergence(initial, pr):
	tempa = []
	tempb = []
	for keys in initial.keys():
		tempa.append(pr[keys])
		tempb.append(initial[keys])
	kld = entropy(tempa, tempb)
	print("%%%%%%%%%%%%%%%")
	print(kld)

def deserved_Exp():
	with open('RatingInfo.csv', 'r') as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			if row[0] == '':
				continue
			RatingInfo [row[0]] = float(row[1])
	sum_of_ratings = sum(list(RatingInfo.values()))
	num_of_movies =  len(list(RatingInfo.values()))

	DeservedExp = {}
	for movie in RatingInfo.keys():
		DeservedExp[movie] = RatingInfo[movie]/sum_of_ratings
	sum_deserved_exp = sum(list(DeservedExp.values()))
	print(sum_deserved_exp)
	json.dump(DeservedExp, open('DeservedExposure.json', 'w'))
	return DeservedExp


def exposure_Analysis(initial):
	pr = nx.pagerank(G, personalization = PopularityExp, alpha = 0.85, max_iter = 1000)
	with open('RatingInfo.csv', 'r') as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			if row[0] == '':
				continue
			RatingInfo [row[0]] = float(row[1])
	print(sum(list(pr.values())))
	sorted_similarity = sorted(list(pr.items()), key=operator.itemgetter(1), reverse = True)
	print(sorted_similarity[:10])
	print("HERE IS THE SUM")
	print(sum(list(pr.values())))
	Exposure_Bias = {'Over_Exposed': [], 'Under_Exposed': [], 'Fairly_Exposed': []}
	num_nodes = len(list(initial.keys()))
	count = 0
	sums = []
	PopFail = []
	UnPopSucc = []
	with tqdm(total=num_nodes) as pbar:
		for key in initial.keys():
			#if RatingInfo[key]> 4.0:
			sums.append(abs (pr[key]-initial[key]))
			#sums.append(math.log(max(pr[key]/initial[key], initial[key]/pr[key])))
			if initial[key] == 0.0:
				Exposure_Bias['Over_Exposed'].append(key)
				count += 1
			elif pr[key]/initial[key]< 0.8:
				Exposure_Bias['Under_Exposed'].append(key)
				if RatingInfo[key]>= 3.5:
					PopFail.append(Movies[key]+' '+str(pr[key]/initial[key]))
			elif pr[key]/initial[key]> 1.2:
				Exposure_Bias['Over_Exposed'].append(key)
				if RatingInfo[key]<= 2.0:
					UnPopSucc.append(Movies[key]+' '+str(pr[key]/initial[key]))
			else:
				Exposure_Bias['Fairly_Exposed'].append(key)
			pbar.update(1)
	fp1 = open('PopFail.txt', 'w')
	fp2 = open('UnPopSucc.txt', 'w')
	for element in PopFail:
		fp1.write(element)
		fp1.write('\n')	
	for element in UnPopSucc:
		fp2.write(element)
		fp2.write('\n')	
	print(len(Exposure_Bias['Over_Exposed'])/float(num_nodes))
	print(len(Exposure_Bias['Fairly_Exposed'])/float(num_nodes))
	print(len(Exposure_Bias['Under_Exposed'])/float(num_nodes))
	
	print(count)
	print(sum(sums))
	divergence(initial, pr)
	#Consistency(pr)

def create_RIN():
	for key in Recommendations.keys():
		neighbors = Recommendations[key]
		#G.add_node(key, name = Movies[key])
		for movie in neighbors[:10]:
			#G.add_node(movie, name = Movies[movie])
			G.add_edge(key, movie)
	#fh = open('ML.edgelist', 'wb')
	#nx.write_edgelist(G, fh, data = False)

def main():
	create_RIN()
	InDeg = G.in_degree()
	print(nx.info(G))
	#json.dump(InDeg, open('InDeg.json', 'w'))
	initial = deserved_Exp()
	exposure_Analysis(initial)


if __name__=='__main__':
	main()
