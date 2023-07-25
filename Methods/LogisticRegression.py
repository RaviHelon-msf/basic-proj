from collections import Counter
import numpy as np

def sigmoid(X, y, W, b, N, alpha):
    y_lin = np.dot(X,W)+b
    y_sig = 1/(1+np.exp(-y_lin))

    delta = y_sig-y
    J = (1/N)*np.sum([d**2 for d in delta])

    dj_dw = (2/N)*np.dot(X.T, delta)
    dj_db = (2/N)*np.sum(delta)

    W = W - alpha*dj_dw
    b = b - alpha*dj_db

    return J, W, b



class LogisticRegression:
    def __init__(self, alpha = 0.01, eta = 1e-5, costFunc = sigmoid):
        self.alpha = alpha
        self.eta = eta
        self.costFunc = costFunc

    def fit(self, X, Y, normalization = max):
        X = np.array(X)

        self.norm_x = [normalization(x) for x in X.T]
        num_samples, num_features = X.shape

        X = X/self.norm_x
        
        W = np.zeros(num_features)
        B = 0

        Jo = 0
        
        flag = True
        delta = 1
        
        while True:
            J, W, B = self.costFunc(X, Y, W, B, num_samples, self.alpha)

            delta = Jo - J

            if(delta<self.eta):
                if flag is False:                
                    print(f"The algorithm is not converging. Cost function moved by {delta}: From {Jo} to {J}")
                    if input("Should we resume execution? (Y/N; default No):") != "Y":
                        break
                flag = False
        
            Jo = J

        print(f"Alforithm converged to a cost function value of {J}")
        self.W = W
        self.B = B


    def predict(self, X, Threshold = 0.5):
        X = X/self.norm_x
        y = [self._predict(x, Threshold) for x in X]
        return np.array(y)

        

    def _predict(self, x, th):
        y_lin = np.dot(x,self.W) + self.B
        y_sig = 1/(1+np.exp(-y_lin))
        return (y_sig>=th)


if __name__ == "__main__":
    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(['#FF0000', '#00FF00'])

    bc = datasets.load_breast_cancer()
    X, Y = bc.data, bc.target
    
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=1234
    )

    predictor = LogisticRegression()
    predictor.fit(X_train,Y_train)
    y_hat = predictor.predict(X_test)
    print(f"Our acc is: {np.sum(Y_test == y_hat) / len(Y_test)}")

    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.suptitle('Visualization of accuracy')

    ax1.scatter(X_test[:,0],X_test[:,1], c=Y_test,cmap=cmap,edgecolor='k',s=20)
    ax1.set_ylabel('True Labels')

    ax2.scatter(X_test[:,0],X_test[:,1], c=y_hat,cmap=cmap,edgecolor='k',s=20)
    ax2.set_ylabel('Predicted Labels')

    plt.show()

