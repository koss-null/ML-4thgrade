import LinearRegressionLab2.item as item
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ItemKeeper:
    def __init__(self, filename):
        file = open(filename, "r")
        lines = file.readlines()
        self.items = []
        for line in lines:
            nums = list(map(lambda arr: float(arr), line.split(",")))
            self.items.append(item.Item(nums))

    def Normalise(self):
        maxX0 = max(map(lambda i: i.params[0], self.items))
        maxX1 = max(map(lambda i: i.params[1], self.items))
        maxY  = max(map(lambda i: i.price, self.items))
        for item in self.items:
            item.params[0] /= maxX0
            item.params[1] /= maxX1
            item.price /= maxY

    def DrawData(self, additionalData):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x, y, z = [], [], []
        for item in self.items:
            x.append(item.params[0])
            y.append(item.params[1])
            z.append(item.price)

        ax.set_xlabel('θ1 : square')
        ax.set_ylabel('θ2 : rooms')
        ax.set_zlabel('Price')
        ax.scatter(x, y, z, c='r', marker='o')
        plt.show()

