from collections import Counter
import numpy as np

import sys

# Sigmoid NOT working
def sigmoid(x): 
    a = 1/(1+np.exp(-x))
    return a

def unit_step(x):
    return np.where(x>=0, 1, 0)

class layer:
    def __init__(self, nodes=5, activation = unit_step):
        self.nodes = nodes
        self.activation = activation
        self.weigths = None

    def f_propagate(self, x, flag=False):
        self.x = np.append(np.array([1]), x)
        
        if flag == False:
            num_features = len(self.x)
            self.weigths = np.zeros((self.nodes, num_features))

        return self.activation(np.dot(self.weigths,self.x))

    def b_propagate(self, delta):
        self.weigths = self.weigths + delta*self.x.T
        


class perceptron:
    def __init__(self, alpha = 0.01, epoch = 1000, activation = unit_step):
        self.alpha = alpha
        self.epoch = epoch
        self.layers = layer(1,activation=activation)

    def fit(self, X, Y, normalization = max):
        self.norm_x = [normalization(x) for x in X.T]
        X = X/self.norm_x

        for _ in range(self.epoch):
            flag = False
            for id, x in enumerate(X):
                y_hat = self.layers.f_propagate(x, flag)
                delta = (Y[id]-y_hat)*self.alpha
                self.layers.b_propagate(delta)
                if flag == False: flag = True

    
    def predict(self, X, Threshold = 0.5):
        X = X/self.norm_x
        y = [self._predict(x, Threshold) for x in X]
        return y

    def _predict(self, x, th):
        y_sig = self.layers.f_propagate(x, True)
        return 1 if y_sig>=th else 0

if __name__ == "__main__":
    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(['#FF0000', '#00FF00'])

    X, Y = datasets.make_blobs(n_samples=150,n_features=2,centers=2,cluster_std=1.05,random_state=2)
    
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=1234
    )

    predictor = perceptron()
    predictor.fit(X_train,Y_train)
    y_hat = predictor.predict(X_test)
    print(f"Our acc is: {(np.sum(Y_test == y_hat))/len(Y_test)}")

    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.suptitle('Visualization of accuracy')

    ax1.scatter(X_test[:,0],X_test[:,1], c=Y_test,cmap=cmap,edgecolor='k',s=20)
    ax1.set_ylabel('True Labels')

    ax2.scatter(X_test[:,0],X_test[:,1], c=y_hat,cmap=cmap,edgecolor='k',s=20)
    ax2.set_ylabel('Predicted Labels')

    plt.show()

