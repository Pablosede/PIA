class AdalineGD(object):
    """ADAptive LInear NEuron classifier.

    Parámetros
    ------------
    eta : float
      ratio de aprendizaje (entre 0.0 y 1.0)
    n_iter : int
      Pasadas sobre el dataset de entrenamiento. (también se llaman épocas)
    random_state : int
      Semilla para el generador de números aleatorios
	  para inicializar el vector de pesos de forma aleatoria

    Atributos
    -----------
    w_ : 1d-array
      Pesos después del entrenamiento.
    cost_ : list
      Valor de la función de coste "suma de los cuadrados" en cada época

    """
    def __init__(self, eta=0.01, epocas=50, random_state=3):
        self.eta = eta
        self.epocas = epocas
        self.random_state = random_state

    def fit(self, X, y):
        
        rgen = np.random.RandomState(self.random_state)
        self.w_ = rgen.normal(loc=0.0, scale=0.01, size=1 + X.shape[1])
        self.cost_ = []

        for i in range(self.epocas):
            net_input = self.net_input(X)
            # Ten en cuenta que el método "activación" no produce ningún efecto 
            # sobre el código, puesto que es simplemente una función de identidad. 
            # En su lugar, podemos escribir directamente `output = self.net_input(X)`.
            # El objetivo de la activación es más conceptual, por ejemplo,   
            # en el caso de una regresión logística (como veremos más tarde), 
            # podríamos cambiarla a 
            # una función sigmoide para implementar un clasificador de regresión logística.
            output = self.activation(net_input)
            errors = (y - output)
            matrizvector=X.T.dot(errors)
            self.w_[1:] += self.eta * matrizvector
            self.w_[0] += self.eta * errors.sum()
            cost = (errors**2).sum() / 2.0
            self.cost_.append(cost)
        return self

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def activation(self, X):
        """Compute linear activation"""
        return X

    def predict(self, X):
        """Retorna la etiqueta de clase después de un paso"""
        return np.where(self.activation(self.net_input(X)) >= 0.0, 1, -1)



from matplotlib.colors import ListedColormap
from sklearn.utils import shuffle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_decision_regions(X, y, classifier, resolution=0.02):

    # setup marker generator and color map
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    # plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.3, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    # plot class samples
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], 
                    y=X[y == cl, 1],
                    alpha=0.8, 
                    c=colors[idx],
                    marker=markers[idx], 
                    label=cl, 
                    edgecolor='black')


df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', header=None)
df.tail()

y = df.iloc[0:100, 4].values
y = np.where(y == 'Iris-setosa', -1, 1)
print(y)
X= df.iloc[0:100, [0,2]].values
print(X)
X, y = shuffle(X, y, random_state=3)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

ada1 = AdalineGD(epocas=10, eta=0.01).fit(X, y)
ax[0].plot(range(1, len(ada1.cost_) + 1), np.log10(ada1.cost_), marker='o')
ax[0].set_xlabel('épocas')
ax[0].set_ylabel('log(suma de los errores cuadrados)')
ax[0].set_title('Adaline - ratio de aprendizaje 0.01')

ada2 = AdalineGD(epocas=10, eta=0.0001).fit(X, y)
ax[1].plot(range(1, len(ada2.cost_) + 1), ada2.cost_, marker='o')
ax[1].set_xlabel('épocas')
ax[1].set_ylabel('suma de los errores cuadrados')
ax[1].set_title('Adaline - ratio de aprendizaje 0.0001')

plt.show()




#ESCALADO DE CARACTERISTICAS (NORMALIZACIÓN)
X_std = np.copy(X)
X_std[:, 0] = (X[:, 0] - X[:, 0].mean()) / X[:, 0].std()
X_std[:, 1] = (X[:, 1] - X[:, 1].mean()) / X[:, 1].std()


#Entrenamiento
ada = AdalineGD(epocas=15, eta=0.01)
ada.fit(X_std, y)


#plot
plot_decision_regions(X_std, y, classifier=ada)
plt.title('Adaline - Descenso del gradiente')
plt.xlabel('longitud del sépalo [normalizado]')
plt.ylabel('longitud del pétalo [normalizado]')
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

plt.plot(range(1, len(ada.cost_) + 1), ada.cost_, marker='o')
plt.xlabel('épocas')
plt.ylabel('Suma de los errores cuadrados')

plt.tight_layout()
plt.show()


#ejemplo multiplicacion matriz vector
matriz=np.array([[1,2],[3,4],[5,6]])
vector=np.array([7,8,9])
result=matriz.T.dot(vector)
print(result)

