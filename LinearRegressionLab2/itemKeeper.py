import LinearRegressionLab2.item as item


class ItemKeeper:
    def __init__(self, filename):
        file = open(filename, "r")
        lines = file.readlines()
        self.items = []
        for line in lines:
            nums = map(lambda arr: int(arr), line.split(","))
            self.items.append(item.Item(nums))