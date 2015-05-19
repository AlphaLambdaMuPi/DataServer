import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

X, Y, Z = [], [], []
X2, Y2, Z2 = [], [], []

f = open('mono.txt')
for l in f:
    x, y, z = [float(i) for i in l.strip('\n').split()]
    X.append(x)
    Y.append(y)
    Z.append(z)

f = open('stereo.txt')
for l in f:
    x, y, z = [float(i) for i in l.strip('\n').split()]
    X2.append(x)
    Y2.append(y)
    Z2.append(z)

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.scatter(X, Y, Z)
ax.scatter(X2, Y2, Z2, c='r')
plt.show()
