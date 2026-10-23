import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', header=None)
print(df.tail())

# Cogemos las 100 primeras filas y generamos un array para poner -1 a las setosas y 1 a versicolor
y_con_etiqueta = df.iloc[0:100,4].values
y = np.where(y_con_etiqueta == 'Iris-setosa', -1, 1)
# print(y_con_etiqueta)
print(y)

# Las características se suelen denotar con la variable X
X = df.iloc[0:150,[0,2]].values
print(X)

plt.scatter(X[:50, 0], X[:50, 1], color='red', marker='o', label='setosa')
plt.scatter(X[50:100, 0], X[50:100, 1], color='blue', marker='x', label='versicolor')
plt.scatter(X[100:150, 0], X[100:150, 1], color='green', marker='^', label='virginica')
plt.legend(loc='upper left')
plt.xlabel('longitud de sépalo [cm]')
plt.ylabel('longitud de pétalo length [cm]')
plt.show()

class perceptron:
    def __init__(self, ratio = 0.01, epocas = 100, semilla = 1):
        self.epocas = epocas
        self.ratio = ratio
        self.semilla = semilla
        rgen = np.random.RandomState(semilla)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=1+X.shape[1])
        self.errores_ = []

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]*1

    def predict(self, X):
        return np.where(self.net_input(X) >= 0, 1, -1)

    def fit(self, X, y):
        for i in range(self.epocas):
            errors = 0
            for xi, target in zip(X, y):
                update = self.ratio * (target - self.predict(xi))
                self.w_[1:] += update * xi
                self.w_[0] += update
                if update != 0:
                    errors += 1
            # fin de las muestras
            self.errores_.append(errors)
        # termina el bucle de epocas
        return self

miPerceptron = perceptron(ratio = 0.1, epocas = 10, semilla = 1)
miPerceptron.fit(X, y)
plt.plot(range(1,len(miPerceptron.errores_)+1),miPerceptron.errores_, marker='o')
plt.xlabel('epocas')
plt.ylabel('errores')
plt.show()


