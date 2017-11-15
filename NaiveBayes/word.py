class Word:
    def __init__(self, word):
        self.word = word
        self.frequency = 1.
        self.amount = 1.

    def increase_amount(self):
        self.amount += 1

    def count_frequency(self, amount):
        self.frequency = self.amount / amount
        #print("freq of " + str(self.word) + " is " + str(self.frequency))
