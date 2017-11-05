class Item:
    def __init__(self, area, rooms, price):
        self.x = [area, rooms]
        self.price = price

    def __init__(self, data):
        self.x = data[0:2]
        self.price = data[2]
