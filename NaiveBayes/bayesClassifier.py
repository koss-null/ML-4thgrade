import os
import math
import NaiveBayes.word as www


class BayesClassifier:
    def __init__(self, training_borders):
        self.good_files, self.bad_files = 0, 0
        self.good_words = self.read_words("data", "legit", training_borders)
        self.bad_words = self.read_words("data", "spmsg", training_borders)

    def read_words(self, path, prefix, training_borders):
        words = []
        files = os.listdir(path)
        words_amount = 0
        cur_file_num = 0
        for file in files:
            if training_borders[0] <= cur_file_num <= training_borders[1]:
                cur_file_num += 1
                continue
            cur_file_num += 1

            if prefix in file:
                # counting amount of bad and good files
                if prefix in "legit":
                    self.good_files += 1
                else:
                    self.bad_files += 1

                file = open(path + "/" + file, "r")
                for line in file.readlines():
                    for word in line.split(" "):
                        words_amount += 1
                        try:
                            word_num = int(word)
                            if word_num in words:
                                words[words.index(word_num)].increase_amount()
                            else:
                                words.append(www.Word(word_num))
                        except Exception:
                            continue
                file.close()

        for word in words:
            word.count_frequency(words_amount)

        return words

    def count_word_probability(self, word, type):
        if type == 1:
            return word.amount / len(self.good_words)
        else:
            return word.amount / len(self.bad_words)

    def count_spam_probability(self, word):
        good_frequency, bad_frequency = 0., 0.
        for wrd in self.good_words:
            if wrd.word == word:
                good_frequency = self.count_word_probability(wrd, 1)
                break

        for wrd in self.bad_words:
            if wrd.word == word:
                bad_frequency = self.count_word_probability(wrd, 2)
                break

        return (good_frequency, bad_frequency)

    # returns good probability vs bad probability attitude
    def count_file_class(self, path):
        good_prob, bad_prob = 1, 1
        word_amount = 0
        file = open("data/"+path, "r")
        for line in file.readlines():
            for word in line.split(" "):
                try:
                    word_num = int(word)
                    sp = self.count_spam_probability(word_num)
                    good_prob += math.log(sp[0])
                    bad_prob += math.log(sp[1])
                    # else ignore
                except Exception:
                    continue

        good_prob += math.log(self.good_files)
        bad_prob += math.log(self.bad_files)

        # print("for " + path + " bad prob is " + str(bad_prob) + " good prob is " + str(good_prob))
        print(good_prob / bad_prob)
        return good_prob / bad_prob
