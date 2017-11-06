import LinearRegressionLab2.itemKeeper as ik
import LinearRegressionLab2.regressionMeister as rm


def main():
    keeper = ik.ItemKeeper("prices.data")
    keeper.Normalise()
    #keeper.DrawData([])
    regressionMeister = rm.RegressionMeister(keeper.items, rm.RegrType.DESCENT)
    regressionMeister.MakeLearning()

    for item in keeper.items:
        print(item.params, item.price)

if __name__ == "__main__":
    main()
