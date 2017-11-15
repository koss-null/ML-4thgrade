import os
import NaiveBayes.word as www

class BayesClassifier:
    def __init__(self):
        self.good_words = self.read_words("data", "legit")
        self.bad_words = self.read_words("data", "spmsg")

    def read_words(self, path, prefix):
        words = []
        files = os.listdir(path)
        words_amount = 0
        for file in files:
            if prefix in file:
                file = open(path + "/" + file, "r")
                for line in file.readlines():
                    for word in line.split(" "):
                        words_amount += 1
                        try:
                            word_num = int(word)
                            if word_num in words:
                                for i in range(0, len(words)):
                                    if words[i].word == word_num:
                                        words[i].increase_amount()
                            else:
                                words.append(www.Word(word_num))
                        except Exception:
                            continue
                file.close()

        for word in words:
            word.count_frequency(words_amount)

        return words

    # 0 - spam
    # 1 - not spam
    def count_spam_probability(self, word):
        good_frequency, bad_frequency = 0., 0.
        for wrd in self.good_words:
            if wrd.word == word:
                good_frequency = wrd.frequency
                break

        for wrd in self.bad_words:
            if wrd.word == word:
                bad_frequency = wrd.frequency
                break

        if bad_frequency == good_frequency:
            return 0.5
        return bad_frequency / (good_frequency + bad_frequency)

    def count_file_class(self, path):
        bad_prob = 0
        word_amount = 0
        file = open("test/"+path, "r")
        for line in file.readlines():
            for word in line.split(" "):
                try:
                    word_num = int(word)
                    bad_prob += self.count_spam_probability(word_num)
                    word_amount += 1
                    # else ignore
                except Exception:
                    continue

        print("for " + path + " bad prob is " + str(bad_prob / word_amount))
        if bad_prob / word_amount > 0.5:
            return 0

        return 1
