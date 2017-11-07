import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import time
import LinearRegressionLab2.item as item


class ItemKeeper:
    def __init__(self, filename):
        self.maxX0, self.maxX1, self.maxY = 1, 1, 1

        self.fig = plt.figure()
        plt.show(block=False)

        file = open(filename, "r")
        lines = file.readlines()
        self.items = []
        for line in lines:
            nums = list(map(lambda arr: float(arr), line.split(",")))
            self.items.append(item.Item(nums))

        self.x, self.y, self.z = [], [], []


    def Normalise(self, normPrice):
        self.maxX0 = max(map(lambda i: i.params[0], self.items))
        self.maxX1 = max(map(lambda i: i.params[1], self.items))
        self.maxY = max(map(lambda i: i.price, self.items)) if normPrice else 1
        for item in self.items:
            item.params[0] /= self.maxX0
            item.params[1] /= self.maxX1
            item.price /= self.maxY

        for itm in self.items:
            self.x.append(itm.params[0])
            self.y.append(itm.params[1])
            self.z.append(itm.price)


    def DrawData(self, additionalData, iter):
        plt.close(self.fig)
        self.fig = plt.figure()
        self.fig.canvas.draw()
        ax = self.fig.add_subplot(111, projection='3d')

        ax.set_xlabel('θ1 : square')
        ax.set_ylabel('θ2 : rooms')
        ax.set_zlabel('Price, iter=' + str(iter))
        ax.scatter(self.x, self.y, self.z, c='r', marker='o')

        x, y, z = [], [], []
        for item in additionalData:
            x.append(item[0])
            y.append(item[1])
            z.append(item[2])
        ax.scatter(x, y, z, c='b', marker='^')
        self.fig.canvas.draw()
        plt.pause(0.0001)
