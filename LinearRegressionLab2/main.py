import LinearRegressionLab2.itemKeeper as ik
import LinearRegressionLab2.regressionMeister as rm


def main():
    keeper = ik.ItemKeeper("prices.data")
    keeper.Normalise(False)
    regressionMeister = rm.RegressionMeister(keeper.items, rm.RegrType.DESCENT)
    regressionMeister.Make_learning()

    learnedCost = []
    for item in keeper.items:
        learnedCost.append([item.params[0], item.params[1], regressionMeister.Find_cost(item.params)])
        print(item.params, item.price, " delta is ", (item.price - learnedCost[len(learnedCost) - 1][2]) * keeper.maxY)

    keeper.DrawData(learnedCost)

if __name__ == "__main__":
    main()
