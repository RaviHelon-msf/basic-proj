import numpy as np
from collections import Counter

name = 1

def entropy(Y):
    E = 0
    for y in np.unique(Y):
        p = np.count_nonzero(Y==y)/len(Y)
        if p>0:
            E -= p*np.log(p)
    return E

class Node:
    def __init__(self,feat = (None, None),leftNode = None, rightNode = None,*,Value = None):
        if Value is not None:
            self.Value = Value
        else:
            self.feature, self.threshold = feat
            self.left = leftNode
            self.right = rightNode
            self.Value = None
        
        global name 
        self.name = name
        name = name+1

    def value(self, x):
        if self.Value is not None:
            print(f"Node: {self.name}, with Value {self.Value}")
            return self.Value
        else:
            print(f"Node: {self.name}, with feature {self.feature} and Threshold {self.threshold}, for X = {x}")
        
            if x[self.feature] > self.threshold:
                print("right")
                return self.right.value(x)
            else:
                print("left")
                return self.left.value(x)

class Tree:
    def __init__(self,minSplit = 2, maxDepth = 100,numFeatures = None):
        self.minSplit = minSplit
        self.max_depth = maxDepth
        self.num_feat = numFeatures

    def fit(self, X, Y):
        num_features = X.shape[1]
        self.num_feat = num_features if not self.num_feat else min(self.num_feat,num_features)

        self.thresholds = []

        y_ = np.unique(Y)
        num_th_max = np.floor(self.max_depth/self.num_feat)

        for idx in range(self.num_feat):
            X_ = np.unique(X[:,idx])
            
            if len(X_)>num_th_max:
                X_ = np.linspace(np.min(X_),np.max(X_),num_th_max)
            
            for x in X_:
                self.thresholds.append((idx,x))
        
        self.root = self._call_Node(X,Y, 1)

    def _call_Node(self,X, Y,depth):
        if depth >= self.max_depth or len(np.unique(Y))==1 or X.shape[0]<=2:
            counter = Counter(Y)
            value = counter.most_common(1)[0][0]
            return Node(Value=value)


        best = (self.thresholds[1])
        E = 2
        idpop = 1

        for id, f in enumerate(self.thresholds):
            idx, th = f
            idth = np.where(X[:,idx]>th,1,0)
            E_ = entropy(Y[idth])
            idth = np.where(idth,0,1)
            _E = entropy(Y[idth])
            Em = 0.5*(_E+E_)
            print(Em)
            if Em < E:
                best = (idx, th)
                E = Em
                idpop = id

        idx, th = best

        self.thresholds.pop(idpop)
        idth_ = np.where(X[:,idx]>th,1,0)
        _idth = np.where(idth_,0,1)

        return Node((idx,th),self._call_Node(X[_idth],Y[_idth],depth+1), self._call_Node(X[idth_],Y[idth_],depth+1))

    def predict(self, X):
        y = [self._predict(x) for x in X]
        return np.array(y)
    
    def _predict(self,X):
        return self.root.value(X)


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

    predictor = Tree()
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