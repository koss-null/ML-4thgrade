import time

from enum import Enum


class RegrType(Enum):
    DESCENT = 1
    GENETIC = 2


class RegressionMeister:
    def __init__(self, items, regressionType):
        self.items = items
        self.regrFunc = self.stubFunc

        if regressionType == RegrType.DESCENT:
            self.regrFunc = self.gardientDescent
        elif regressionType == RegrType.GENETIC:
            self.regrFunc = self.genericRegression

    def stubFunc(self):
        print("not implemented yet")

    def gardientDescent(self):
        self.stubFunc()

    def genericRegression(self):
        self.stubFunc()

    def MakeLearning(self):
        start = time.time()
        self.regrFunc()
        end = time.time()
        print("Learning have been executing for ", end - start)

