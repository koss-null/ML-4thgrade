class Item:
    def __init__(self, area, rooms, price):
        self.area, self.rooms, self.price = area, rooms, price

    def __init__(self, data):
        self.area, self.rooms, self.price = data[0], data[1], data[2]