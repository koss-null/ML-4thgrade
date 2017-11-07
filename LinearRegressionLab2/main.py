import LinearRegressionLab2.itemKeeper as ik
import LinearRegressionLab2.regressionMeister as rm
from functools import reduce


def main():
    keeper = ik.ItemKeeper("prices.data")
    keeper.Normalise(False)
    regressionMeister = rm.RegressionMeister(keeper.items, rm.RegrType.GENETIC)
    regressionMeister.Make_learning()

    learnedCost = []
    delta = 0
    for item in keeper.items:
        learnedCost.append([item.params[0], item.params[1], regressionMeister.Find_cost(item.params)])
        delta += abs(item.price - learnedCost[len(learnedCost) - 1][2]) * keeper.maxY
    delta /= len(keeper.items)

    print("Average accuracy is ", delta)
    items = list(map(lambda x: x.price, keeper.items))
    avgCost = reduce(lambda x, y: x + y, items) / len(keeper.items)
    print("Average house cost is ", avgCost, " accurancy is ", delta / avgCost * 100, "%")

    keeper.DrawData(learnedCost)

if __name__ == "__main__":
    main()
