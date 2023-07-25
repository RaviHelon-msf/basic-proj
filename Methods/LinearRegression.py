
import numpy as np

def LSE_cost(X, Y, W, B, N, alpha):
    delta = (np.dot(X,W)+B) - Y
    J = (1/N)*np.sum([d**2 for d in delta])

    dj_dw = (2/N)*np.dot(X.T, delta)
    dj_db = (2/N)*np.sum(delta)

    W = W - alpha*dj_dw
    B = B - alpha*dj_db

    return J, W, B

class Linear_Regressor:
    def __init__(self, alpha = 0.01, eta = 1e-15):
        self.alpha = alpha
        self.eta = eta

    def fit(self, X, Y, normalization = max, costfunc = LSE_cost):
        Y = np.array(Y)
        X = np.array(X)

        self.norm_x = [normalization(x) for x in X.T]
        self.norm_y = normalization(Y)
        num_samples, num_features = X.shape

        X = X/self.norm_x
        Y = Y/self.norm_y

        self.W = np.zeros(num_features)
        self.B = 0

        self.J = 0
        
        print(f"Alforithm started with a cost function value of {self.J}")
        flag = True
        delta = 1
        while True:
            J, self.W, self.B = costfunc(X, Y, self.W, self.B, num_samples, self.alpha)

            delta = self.J - J

            if(delta<self.eta):
                if flag is False:                
                    print(f"The algorithm is not converging. Cost function moved by {delta}: From {self.J} to {J}")
                    if input("Should we resume execution? (Y/N):") != "Y":
                        break
                flag = False
                
        
            self.J = J

        print(f"{self.W.shape} Alforithm converged to a cost function value of {self.J}")


    def predict(self, X):
        X = X/self.norm_x
        y = np.dot(X,self.W) + self.B
        y = y*self.norm_y
        return y


def r2_score(y_true, y_pred):
    corr_matrix = np.corrcoef(y_true, y_pred)
    corr = corr_matrix[0, 1]
    return corr ** 2


if __name__ == "__main__":
    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    import matplotlib.pyplot as plt

    X, Y = datasets.make_regression(n_samples=100,n_features=1,noise=40,random_state=4)
    
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=1234
    )

    predictor = Linear_Regressor()
    predictor.fit(X_train,Y_train)
    y_hat = predictor.predict(X_test)

    print(f"{Y_test.shape}{y_hat.shape}{X_test.shape}")

    print(f"Our acc is: {r2_score(Y_test, y_hat)}")

    fig = plt.figure(figsize=(8, 6))
    m1 = plt.scatter(X_train, Y_train)
    m2 = plt.scatter(X_test, Y_test)
    plt.plot(X_test, y_hat, color="black", linewidth=2, label="Prediction")
    plt.show()