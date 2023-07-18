from collections import Counter
import numpy as np

def euclidian(x1, x2): 
    return np.sqrt(np.sum((x1-x2)**2))

class KNN:
    def __init__(self, k=3, distance = euclidian):
        self.k = k
        self.distance = distance

    def fit(self, X, Y):
        self.train_X = X
        self.train_Y = Y

    def predict(self, X):
        y = [self._predict(x) for x in X]
        return np.array(y)

    def _predict(self, x):
        distances = [self.distance(x,xtrain) for xtrain in self.train_X]
        k_ind = np.argsort(distances)[0:self.k]
        y = Counter(self.train_Y[k_ind]).most_common(1)
        return y[0][0]



if __name__ == "__main__":
    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

    iris = datasets.load_iris()
    X, Y = iris.data, iris.target

    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=1234
    )

    predictor = KNN()
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


