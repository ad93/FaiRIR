"""
We have taken the implementation of iFair from the authors directly.
"""
import numpy as np
from ifair_impl.lowrank_helpers import iFair as ifair_func
from ifair_impl.lowrank_helpers import predict as ifair_predict
import sklearn.metrics.pairwise as pairwise
from sklearn.preprocessing import normalize
from scipy.optimize import minimize

class iFair:

    def __init__(self, k=20, A_x=1.0, A_z=0.01, max_iter=10, nb_restarts=3, task='regression'):
        self.k = k
        self.A_x = A_x
        self.A_z = A_z
        self.max_iter = max_iter
        self.nb_restarts = nb_restarts
        self.opt_params = None
        self.task = task
        print('I am in constructor')

    def fit(self, X_train, dataset=None):
        """
        Learn the model using the training data.

        :param X:     Training data.
        """
        print('Fitting iFair...')
        ##if dataset object is not passed, assume that there is only 1 protected attribute and it is the last column of X
        '''if dataset:
            D_X_F = pairwise.euclidean_distances(X_train[:, dataset.nonsensitive_column_indices], X_train[:, dataset.nonsensitive_column_indices])
            l = len(dataset.nonsensitive_column_indices)
        else:
            D_X_F = pairwise.euclidean_distances(X_train[:, :-1],
                                                 X_train[:, :-1])
            l = X_train.shape[1] - 1'''
        D_X_F = pairwise.cosine_distances(X_quality)
        l = X_train.shape[1]
        P = X_train.shape[1]
        min_obj = None
        opt_params = None
        for i in range(self.nb_restarts):
            x0_init = np.random.uniform(size=P * 2 + self.k + P * self.k)
            #setting protected column weights to epsilon
            ## assumes that the column indices from l through P are protected and appear at the end
            for i in range(l, P, 1):
                x0_init[i] = 0.0001    
            bnd = [(None, None) if (i < P * 2) or (i >= P * 2 + self.k) else (0, 1)
                   for i in range(len(x0_init))]
            opt_result = minimize(ifair_func, x0_init,
                                  args=(X_train, D_X_F, self.k, self.A_x, self.A_z, 0),
                                  method='L-BFGS-B',
                                  jac=False,
                                  bounds=bnd,
                                  options={'maxiter': self.max_iter,
                                           'maxfun': self.max_iter,
                                           'eps': 1e-3})
            
            if (min_obj is None) or (opt_result.fun < min_obj):
                min_obj = opt_result.fun
                opt_params = opt_result.x
                print('I am here')
        self.opt_params = opt_params

    def transform(self, X):
        X_hat = ifair_predict(self.opt_params, X, k=self.k)
        return X_hat

    def fit_transform(self, X_train, dataset=None):
        """
        Learns the model from the training data and returns the data in the new space.

        :param X:   Training data.
        :return:    Training data in the new space.
        """
        print('Fitting and transforming...')
        self.fit(X_train, dataset)
        return self.transform(X_train)

Node_Embedding = {}
f = open('QualityGraph.emb', 'r')
for line in f:
        if len(line.split(' ')) == 2:
                continue
        vertexid = int(line.split(' ')[0])
        vector = list(map(float, line.split(' ')[1:]))
        Node_Embedding[vertexid] = vector

f.close()
Nodes = []
Embeddings = []
for node in sorted(Node_Embedding.keys()):
        Embeddings.append(Node_Embedding[node])
        Nodes.append(node)
X_quality = normalize(np.array(Embeddings))
