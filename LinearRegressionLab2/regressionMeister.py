import time
from enum import Enum


class RegrType(Enum):
    DESCENT = 1
    GENETIC = 2


class RegressionMeister:
    def __init__(self, items, regressionType):
        self.items = self.normalise(items)
        self.regrFunc = self.stubFunc

        if regressionType == RegrType.DESCENT:
            self.regrFunc = self.gardientDescent
        elif regressionType == RegrType.GENETIC:
            self.regrFunc = self.genericRegression

    def stubFunc(self):
        print("not implemented yet")

    def normalise(self, items):
        maxX0 = max(map(lambda i: i.x[0], items))
        maxX1 = max(map(lambda i: i.x[1], items))
        for item in items:
            item.x[0] /= maxX0
            item.x[1] /= maxX1

        return items

    def gardientDescent(self):
        self.stubFunc()

    def genericRegression(self):
        self.stubFunc()


    def MakeLearning(self):
        start = time.time()
        self.regrFunc()
        end = time.time()
        print("Learning have been executing for ", end - start)

