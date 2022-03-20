import csv 
from gensim.models import Word2Vec
from gensim.models import KeyedVectors


Users = {}


with open('ratings.dat', 'r') as CSV_file:
	reader = CSV_file.readlines()
	for row in reader:
		row = row.strip().split("::")
		if row[0] == 'userId':
			print(row)
			continue
		if row[0] not in Users.keys():
			Users[row[0]]= [row[1]]
		else:
			Users[row[0]].append(row[1])
		

#print(list(Users.values()))

model = Word2Vec(list(Users.values()), size = 128, min_count=0, negative = 15, sg = 1, hs = 0, iter = 50)

words = list(model.wv.vocab)
absent = []

word_vectors = model.wv


model.save('model.bin')

new_model = Word2Vec.load('model.bin')



txtmodel = KeyedVectors.load('model.bin')
model.wv.save_word2vec_format('Movies.emb', binary=False)
