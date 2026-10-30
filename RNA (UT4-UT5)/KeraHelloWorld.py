import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # o "3" para solo errores
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

miModelo = tf.keras.Sequential([keras.layers.Dense(1, input_shape=[1])])
miModelo.compile(optimizer='sgd', loss='mean_squared_error')

xs = np.array([-1, 0, 1, 2, 3, 4], dtype=float)
ys = np.array([-3,-1, 1, 3, 5, 7], dtype=float)

miModelo.fit(xs, ys, epochs=1000)

resultado = miModelo.predict(np.array(xs))
print(resultado)

plt.scatter(xs,ys,marker='o', color='red')
plt.scatter(xs,resultado,marker='x', color='blue')
plt.show()

xPrueba = np.arange(-500, 500, 1)
yPrueba = xPrueba*2 -1

resultado2 = miModelo.predict(np.array(xPrueba))
print(resultado2)
plt.scatter(xPrueba,yPrueba,marker='o', color='red')
plt.scatter(xPrueba,resultado2,marker='x', color='blue')
plt.show()

