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
        self.regrFunc = self.stub_func
        self.learnedThetas = []

        if regressionType == RegrType.DESCENT:
            self.regrFunc = self.gardient_descent
        elif regressionType == RegrType.GENETIC:
            self.regrFunc = self.generic_regression

    @staticmethod
    def stub_func():
        print("not implemented yet")

    @staticmethod
    def deriv_cost_function(hypot, real):
        j = []
        for i in range(0, hypot.size):
            j.append([1])
        I = np.matrix(j)
        # TODO: fixit matrix convertion
        return np.matrix((1/len(hypot)) * ((hypot - real) * I)).item(0)

    @staticmethod
    def cost_function(hypot, real):
        j = []
        for i in range(0, hypot.size):
            j.append([1])
        I = np.matrix(j)
        return (np.power((hypot - real), 2) * I)[0]

    def gardient_descent(self):
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

            cf = math.fabs(self.cost_function(np.matrix(hypots), np.matrix(results)))
            # print("current CostFunc is ", cf, " delta is ", cfLast - cf, " step ", step)
            if math.fabs(cfLast - cf) < 1:
                break
            cfLast = cf

            for i in range(0, len(thetas)):
                # TODO: fix this wierd shit
                for j in range(0, len(params)):
                    hypots[j] *= params[j][i]
                    results[j] *= params[j][i]

                delta = self.alpha * self.deriv_cost_function(np.matrix(hypots), np.matrix(results))
                # converting into np.matrix to get the first item. TODO: FIXIT
                thetas[i] -= np.matrix(delta).item(0)

                for j in range(0, len(params)):
                    hypots[j] /= params[j][i]
                    results[j] /= params[j][i]

        print("Thetas changed into ", thetas)
        self.learnedThetas = thetas


    def generic_regression(self):
        self.stub_func()

    def Find_cost(self, params):
        params = [1] + params[:]
        cost = 0.
        for i in range(0, len(self.learnedThetas)):
            cost += params[i] * self.learnedThetas[i]
        return cost

    def Make_learning(self):
        start = time.time()
        self.regrFunc()
        end = time.time()
        print("Learning have been executing for ", end - start)
