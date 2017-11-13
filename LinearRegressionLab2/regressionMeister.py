import math
import random
import time
from enum import Enum

import numpy as np


class RegrType(Enum):
    DESCENT = 1
    GENETIC = 2


class RegressionMeister:
    defaultThetaVal = 500
    alpha = 0.025

    def __init__(self, items, regressionType, keeper):
        self.items = items
        self.regrFunc = self.stub_func
        self.learnedThetas = []
        self.keeper = keeper

        if regressionType == RegrType.DESCENT:
            self.regrFunc = self.gradient_descent
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
        return np.matrix((1 / len(hypot)) * ((hypot - real) * I)).item(0)

    @staticmethod
    def cost_function(hypot, real):
        j = []
        for i in range(0, hypot.size):
            j.append([1])
        I = np.matrix(j)
        return (np.power((hypot - real), 2) * I)[0]

    def select_cost_function(self, hypot, real):
        j = []
        for i in range(0, hypot.size):
            j.append([1])
        I = np.matrix(j)
        return ((hypot - real) * I).item(0)

    def gradient_descent(self):
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
            cfDifferences = (100, 1000000, 10000000000)
            if math.fabs(cfLast - cf) < cfDifferences[1]:
                print("steps done ", step)
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

            learnedCost = []
            self.learnedThetas = thetas
            for item in self.items:
                learnedCost.append([item.params[0], item.params[1], self.Find_cost(item.params)])
            self.keeper.DrawData(learnedCost, step, 30)

        print("Thetas changed into ", thetas)
        self.learnedThetas = thetas

    def make_hypot(self, x):
        hypot = []
        for item in self.items:
            hypot.append(x[0] + x[1] * item.params[0] + x[2] * item.params[1])
        return hypot

    # selects n best thetas lists
    def selection(self, thetas, n):
        results = []
        for item in self.items:
            results.append(item.price)

        thetas.sort(key=lambda x: abs(self.cost_function(np.matrix(self.make_hypot(x)), np.matrix(results))))
        print("the best result for generation ", self.cost_function(np.matrix(self.make_hypot(thetas[0])), np.matrix(results)))
        return thetas[0:n]

    # gets two theta lists and concatinates them
    def crossover(self, thetas):
        theta = []
        for i in range(0, len(thetas[0])):
            theta.append((thetas[0][i] + thetas[1][i])/2)
        return theta

    # helps to get new thetas
    def mutation(self):
        # WOW! If this shit gonna work, IDK what'll I do
        return [float(random.randint(-1000000, 1000000)), float(random.randint(-1000000, 1000000)), float(random.randint(-1000000, 1000000))]

    def generic_regression(self):
        lastGeneration = 180

        mutationNumber = 1000
        thetas = []
        # generating mutants
        for i in range(0, mutationNumber):
            thetas.append(self.mutation())

        for generation in range(0, lastGeneration):
            print("Generation ", generation)
            thetas = self.selection(thetas, max(int(len(thetas) / 2), 1))

            for i in range(0, int(len(thetas) / 2)):
                thetas.append(self.crossover([thetas[i], thetas[i+1]]))

            for i in range(0, int(len(thetas) / 3)):
                thetas.append(self.mutation())
            print("Generation ", generation, " alive ", len(thetas), " best thetas ", thetas[0])

            learnedCost = []
            self.learnedThetas = thetas[0]
            for item in self.items:
                learnedCost.append([item.params[0], item.params[1], self.Find_cost(item.params)])
            self.keeper.DrawData(learnedCost, generation, 10)

        thetas = self.selection(thetas, 1)
        self.learnedThetas = thetas[0]

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
