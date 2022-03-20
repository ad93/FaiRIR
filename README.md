# Code Base for FaiRIR

### URL to the datasets: 
- MovieLens: https://grouplens.org/datasets/movielens/
- Amazon Review Dataset: http://jmcauley.ucsd.edu/data/amazon/links.html

### Preprocessing files:
- ratingExctracter.py shall extract the ratings from the data files obtained from the above URLs. 

### Vanilla representation learning:
- VanillaSVDRepresentation.py (VanillaI2VRepresentation.py) needs to be run to learn the vanilla representation of items / movies for further processing. 
- input: user-item interaction logs
- output: item representations

### Similarity evaluation:
- simeval.py (similarity_item2vec.py) evaluates the dense similarity between all pairs of item in the datasets. 
- input: learnt representations
- output: A dense matrix of similarity between items

### Related Item Recommendation generation:
- RIR.py generates the recommendation instances provided the similarity matrix obtained in similarity evaluation.
- input: similarity matrix
- output: Related Item Recommendations for each item

### Related Item Network generation:
- RIN.py generates the related item recommendation as discussed in the paper from the related item recommendations. It also performs the exposure analyses of the RINs and provides the exposure bias score. 
- input: related item recommendations
- output: related item network, exposure bias score

### FairRIR neighbor algorithm:
- FaiRIR_nbr.py generates the fair recommendation network from the given desired exposure distribution and relatedness of items. 
- input: similarity matrix among items, desired exposure of items
- output: Fair related item recommendation network

### FairRIR representation learning:
- ./FaiRIR_RL/main.py (main_i2v.py) generates the fair representations learnt by optimizing for relatedness and desiredness loss. For more details, please refer to the paper.
- input: vanilla representations of algorithms, desiredness graph representations
- output: fair representations
- To generate FaiRIR recommendations, please use the RIR.py with new input being the fair representations learnt above.

