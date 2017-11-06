class Item:
    def __init__(self, area, rooms, price):
        self.params = [area, rooms]
        self.price = price

    def __init__(self, data):
        self.params = data[0:2]
        self.params.append(data[0] ** 2, data[1] ** 2)
        self.price = data[2]
