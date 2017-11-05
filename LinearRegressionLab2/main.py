import LinearRegressionLab2.itemKeeper as ik
import LinearRegressionLab2.regressionMeister as rm


def main():
    keeper = ik.ItemKeeper("prices.data")
    regressionMeister = rm.RegressionMeister(keeper.items, rm.RegrType.GENETIC)
    regressionMeister.MakeLearning()


if __name__ == "__main__":
    main()
