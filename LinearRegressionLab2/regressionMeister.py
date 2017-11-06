import time
from enum import Enum
import numpy as np
import math


class RegrType(Enum):
    DESCENT = 1
    GENETIC = 2


class RegressionMeister:
    defaultThetaVal = 500
    alpha = 0.001

    def __init__(self, items, regressionType):
        self.items = items
        self.regrFunc = self.stubFunc

        if regressionType == RegrType.DESCENT:
            self.regrFunc = self.gardientDescent
        elif regressionType == RegrType.GENETIC:
            self.regrFunc = self.genericRegression

    def stubFunc(self):
        print("not implemented yet")

    def derivCostFunction(self, hypot, real):
        j = []
        for i in range(0, hypot.size):
            j.append([1])
        I = np.matrix(j)
        # TODO: fixit matrix convertion
        return np.matrix(1/(2 * len(hypot)) * ((hypot - real) * I)).item(0)

    def costFunction(self, hypot, real):
        j = []
        for i in range(0, hypot.size):
            j.append([1])
        I = np.matrix(j)
        return (np.power((hypot - real), 2) * I)[0]

    def gardientDescent(self):
        # getting ready
        thetas = []
        params = []
        results = []
        for item in self.items:
            # coeff x0=1 is for the first theta
            params.append([1.] + item.params[:])
            results.append(item.price)
        for i in range(0, len(params[0])):
            thetas.append(self.defaultThetaVal)

        # making descent
        step = 0
        cfLast = 0
        while True:
            step += 1
            Thetas = np.matrix(thetas).transpose()
            hypots = []
            for i in range(0, len(params)):
                Params = np.matrix(params[i])
                hypot = (Params * Thetas).item(0)

                hypots.append(hypot)

            cf = math.fabs(self.costFunction(np.matrix(hypots), np.matrix(results)))
            print("current CostFunc is ", cf, " delta is ", cfLast - cf, " step ", step)
            if math.fabs(cfLast - cf) < 10:
                break
            cfLast = cf

            for i in range(0, len(thetas)):
                # TODO: fix this wierd shit
                for j in range(0, len(params)):
                    hypots[j] *= params[j][i]
                    results[j] *= params[j][i]

                delta = self.alpha * self.derivCostFunction(np.matrix(hypots), np.matrix(results))
                # converting into np.matrix to get the first item. TODO: FIXIT
                thetas[i] -= np.matrix(delta).item(0)

                for j in range(0, len(params)):
                    hypots[j] /= params[j][i]
                    results[j] /= params[j][i]

            print("Thetas changed into ", thetas)

    def genericRegression(self):
        self.stubFunc()

    def MakeLearning(self):
        start = time.time()
        self.regrFunc()
        end = time.time()
        print("Learning have been executing for ", end - start)
