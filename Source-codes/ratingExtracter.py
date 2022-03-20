import csv
import pandas as pd
import json 

df = pd.DataFrame(columns=['Average User Rating', 'Number of Votes', 'Liked by'])

movie_rating_info = {}
with open('ratings.dat', 'r') as CSV_file:
	reader = CSV_file.readlines()
	for row in reader:
		row = row.strip().split("::")
		if row[0] == 'userId':
			continue
		if row[1] not in movie_rating_info.keys():
			movie_rating_info[row[1]] = []
			movie_rating_info[row[1]].append(float(row[2]))
			movie_rating_info[row[1]].append(1)
			if float(row[2])>=4.0:
				movie_rating_info[row[1]].append(1)
			else:
				movie_rating_info[row[1]].append(0)
		else:
			movie_rating_info[row[1]][0] += float(row[2])
			movie_rating_info[row[1]][1] += 1
			if float(row[2])>=4.0:
				movie_rating_info[row[1]][2] += 1
	
	#finalset = list()
	for movie in movie_rating_info.keys():
		df.loc[movie, 'Average User Rating'] = movie_rating_info[movie][0]/ movie_rating_info[movie][1]
		df.loc[movie, 'Number of Votes'] = movie_rating_info[movie][1]
		#if movie_rating_info[movie][1] >= 100:
		#	finalset.append(movie)
		df.loc[movie, 'Liked by'] = movie_rating_info[movie][2]/movie_rating_info[movie][1]

#print(len(finalset))
df.to_csv('RatingInfo.csv', encoding = 'utf-8')	
#json.dump(finalset, open('MovieList.txt', 'w'))	
