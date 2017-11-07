import LinearRegressionLab2.itemKeeper as ik
import LinearRegressionLab2.regressionMeister as rm
from functools import reduce


def main():
    keeper = ik.ItemKeeper("prices.data")
    keeper.Normalise(False)
    regressionMeister = rm.RegressionMeister(keeper.items, rm.RegrType.GENETIC, keeper)
    regressionMeister.Make_learning()

    learnedCost = []
    delta = 0
    for item in keeper.items:
        learnedCost.append([item.params[0], item.params[1], regressionMeister.Find_cost(item.params)])
        delta += abs(item.price - learnedCost[len(learnedCost) - 1][2]) / item.price * keeper.maxY * 100
    delta /= len(keeper.items)

    print("AVG error is: ", delta, "%")

    keeper.DrawDataLast(learnedCost)
    while(False):
        x = int(input('What to predict? (square):'))
        y = int(input('What to predict? (rooms):'))
        cost = regressionMeister.Find_cost([x / keeper.maxX0, y / keeper.maxX1])
        print("Your cost is ", cost)

if __name__ == "__main__":
    main()
