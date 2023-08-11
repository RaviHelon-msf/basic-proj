import numpy as np
from collections import Counter

def entropy(Y):
    E = 0
    for y in np.unique(Y):
        p = np.count_nonzero(Y==y)/len(Y)
        if p>0:
            E -= p*np.log2(p)
    return E

class Node:
    def __init__(self,feat = (None, None),leftNode = None, rightNode = None,*,Value = None):
        #print(f"Feature {feat} and Value {Value}")
        self.feature, self.threshold = feat
        self.left = leftNode
        self.right = rightNode
        self.Value = Value

    def value(self, x):
        #print(x)
        if self.Value is not None:
            return self.Value
        else:            
            if x[self.feature] > self.threshold:
                return self.right.value(x)
            else:
                return self.left.value(x)

class Forest:
    def __init__(self,minSplit = 2, maxDepth = 100,numFeatures = None,num_trees = 5, min_info_gain = 0.01):
        self.minSplit = minSplit
        self.max_depth = maxDepth
        self.num_feat = numFeatures
        self.min_info_gain = min_info_gain
        self.root = [0]*num_trees

    def fit(self, X, Y):
        X = np.array(X)
        Y = np.array(Y)
        num_samples, num_features = X.shape
        self.num_feat = num_features if not self.num_feat else min(self.num_feat,num_features)
        
        for r in range(len(self.root)):
            feat_idx = np.random.choice(num_features,num_features-self.num_feat,replace=False)
            sample_idx = np.random.choice(num_samples,num_samples,replace=True)
            Xr = np.zeros((num_samples,num_features))
            for id, idx in enumerate(sample_idx):
                Xr[id] = X[idx]
            for idx in feat_idx:
                Xr[:,idx] = 0
            self.root[r] = self._call_Node(Xr,Y)
            #print(type(self.root[r]))

    def _call_Node(self,X, Y,depth=1, Info_gain=1):
        if depth >= self.max_depth or len(np.unique(Y))==1 or X.shape[0]<=2 or Info_gain < self.min_info_gain or not np.any(X):
            counter = Counter(Y)
            try:
                value = counter.most_common(1)[0][0]
            except IndexError:
                print("Error")
                return Node(Value = 0)
            #print(value)
            return Node(Value=value)

        E = entropy(Y)
        Igain = 0 

        for idx, x in enumerate(X.T):
            #print(x)
            Em = E
            u = np.unique(x)
            if len(u) ==2 :
                th = 0.5*u[0]+0.5*u[1]

                _idl = np.where(x<=th)
                _idr = np.where(x>th)
                
                w = len(_idl)/len(x)
                Em = w*entropy(Y[_idl]) + (1 - w)*entropy(Y[_idr])
                
            elif len(u) > 2:
                Em, _idl, _idr, th = self.best_th(x,Y)

            I = E - Em
            if I > Igain:
                #print(f"information gain: {I}")
                idl = _idl
                idr = _idr
                feat = idx
                threshold = th
                Igain = I


        #print(f"finally, the selected is Feature{feat} with the th of {threshold:.2f} and I {Igain}")
        #print(idl)
        #print(X)
        Xl = np.array(X[idl[0]])
        Yl = np.array(Y[idl[0]])
        for id in idl[1:]:            
            Xl = np.append(Xl,X[id],axis=0)
            np.append(Yl,Y[id])
        Xl[:,feat] = 0
        

        Xr = np.array(X[idr[0]])
        Yr = np.array(Y[idr[0]])
        for id in idr[1:]:            
            Xr = np.append(Xr,X[id],axis=0)
            
            np.append(Yr,Y[id])
        Xr[:,feat] = 0
        
        return Node((feat,threshold),self._call_Node(Xl,Yl,depth+1, Igain), self._call_Node(Xr,Yr,depth+1, Igain))

    def best_th(self, x,Y):
        X_ = np.linspace(np.min(x),np.max(x))[1:-2]
        E = 1


        for th in X_:
            _idl = np.where(x<=th)
            _idr = np.where(x>th)
             
            w = len(_idl)/len(x)
            Em = w*entropy(Y[_idl]) + (1 - w)*entropy(Y[_idr])

            #print(f"Entropy {Em:.2f} for the {th:.2f}:  {np.unique(Y[_idl])} and {np.unique(Y[_idr])}")

            if Em < E:
                #print("Selected")
                idl = _idl
                idr = _idr
                threshold = th
                E = Em
        #print("Returned")
        return E, idl, idr, threshold
    
    def predict(self, X):
        y = [self._predict(x) for x in X]
        print(y)
        return np.array(y)
    
    def _predict(self,X):
        s = [root.value(X) for root in self.root]
        counter = Counter(s)
        print(s)
        return counter.most_common(1)[0][0]


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

    predictor = Forest()
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