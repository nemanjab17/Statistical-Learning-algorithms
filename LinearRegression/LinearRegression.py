from pandas import DataFrame, Series, read_csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sklearn.utils import shuffle

df = read_csv('Advertising.csv')
head = ['TV' 'radio' 'newspaper' 'sales']
df = df[(df.sales > 1.2)]


fig, ax = plt.subplots()

x = df['TV']/10
y = df['sales']

def getparameters(x, y, theta0, theta1, iterations, alpha):
    n = float(len(x))
    for i in range(iterations):
        y_current = (theta1*x)+theta0
        cost = sum([data**2 for data in (y-y_current)]) / n
        theta0_gradient = -(2/n)*sum(y-y_current)
        theta1_gradient = -(2/n)*sum(x*(y-y_current))
        theta0 -= (alpha*theta0_gradient)
        theta1 -= (alpha*theta1_gradient)
    return theta0, theta1
        
theta0, theta1 = getparameters(x,y,1.0, 1.0, 100, 0.0001)
ax.scatter(x, y, marker='.')
ax.plot([0, 30], [0, theta0+theta1*30], 'k-', lw=2)
plt.show()
