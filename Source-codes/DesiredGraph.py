import networkx as nx
import csv
import operator 

G = nx.DiGraph()

RatingInfo = {}
with open('RatingInfo.csv', 'r') as csv_file:
	reader = csv.reader(csv_file)
	for row in reader:
		if row[0] == '':
			continue
		RatingInfo [row[0]] = float(row[1])

for node in RatingInfo.keys():
	NodeSim = {}
	Neighbors = []
	for item in RatingInfo.keys():
		NodeSim[item] = abs(RatingInfo[node]-RatingInfo[item])
	sorted_similarity = sorted(list(NodeSim.items()), key=operator.itemgetter(1), reverse = False)
	for element in sorted_similarity[1:11]:
		G.add_edge(node, element[0])

print(nx.info(G))
fh = open('QualityGraph.edgelist', 'wb')
nx.write_edgelist(G, fh, data= False)
