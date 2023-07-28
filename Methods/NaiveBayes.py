from collections import Counter
import numpy as np

def normal(x,mean,var): 
    numerator = np.exp(-((x - mean) ** 2) / (2 * var))
    denominator = np.sqrt(2 * np.pi * var)
    return numerator / denominator

class naive_Bayes:
    def __init__(self, pdf = normal):       
        self.pdf = pdf

    def fit(self, X, Y):
        num_samples, num_features = X.shape
        
        self.classes = np.unique(Y)
        num_classes = len(self.classes)

        self.means = np.zeros((num_classes, num_features), dtype=np.float64)
        self.vars = np.zeros((num_classes, num_features), dtype=np.float64)
        self.priori = np.zeros(num_classes, dtype=np.float64)

        for id, y_class in enumerate(self.classes):
            ind_y = y_class == Y

            self.means[id,:] = X[ind_y].mean(axis=0)
            self.vars[id,:] = X[ind_y].var(axis=0)
            self.priori[id] = sum(ind_y)/num_samples

    def predict(self, X):
        y = [self._predict(x) for x in X]
        return np.array(y)

    def _predict(self, x):
        posterior = []
        for id, _ in enumerate(self.classes):
            mean = self.means[id]
            var = self.vars[id]
            posteriori = np.sum(np.log(self.pdf(x, mean, var))) + np.log(self.priori[id])
            posterior.append(posteriori)
        return self.classes[np.argmax(posterior)]
            
            



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

    predictor = naive_Bayes()
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


