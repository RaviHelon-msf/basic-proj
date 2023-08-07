from collections import Counter
import numpy as np

import sys

def hinge(X, y, W, b, alpha,lbd):
    J = 0

    for idx, xi in enumerate(X):
        y_hat = np.dot(xi,W) - b
        J_ = 1-y[idx]*y_hat

        dw = 2*lbd*W
        db = 0

        if(J_>0):
            dw += np.dot(xi,y[idx])
            db += y[idx]
            J += + J_ 

        W -= alpha*dw
        b -= alpha*db


    J = J/idx + lbd*abs(sum(W))
    return J, W, b

class perceptron:
    def __init__(self, alpha = 1e-3, eta = 1e-8, J = hinge):
        self.alpha = alpha
        self.eta = eta
        self.J = J
        self.lbd = 0

    def regularization(self, lbd = 1e-2):
        self.lbd = lbd

    def fit(self, X, Y, normalization = max):
        self.norm_x = [normalization(abs(x)) for x in X.T]
        X = X/self.norm_x

        y_ = np.where(Y <= 0, -1, 1)
        num_samples, num_features = X.shape

        self.W = np.zeros(num_features)
        self.B = 0

        eta = 100
        J_prio = 5

        while eta > self.eta:
        #for _ in range(1000):
            J_post, self.W, self.B = self.J(X,y_,self.W,self.B, self.alpha,self.lbd)

            eta = abs(J_post-J_prio)
            J_prio = J_post
            
        
    
    def predict(self, X, Threshold = 0.1):
        X = X/self.norm_x
        y = [self._predict(x, Threshold) for x in X]
        return y

    def _predict(self, x, th):
        y_hat = np.dot(x,self.W) - self.B
        return 0 if y_hat>=th else 1

if __name__ == "__main__":
    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(['#FF0000', '#00FF00'])

    X, Y = datasets.make_blobs(n_samples=50,n_features=2,centers=2,cluster_std=1.05,random_state=40)
    
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=1234
    )

    predictor = perceptron()
    predictor.regularization()
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