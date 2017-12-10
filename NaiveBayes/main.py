import NaiveBayes.bayesClassifier as bc
import os
import numpy as np
import shutil


def main():
    files = os.listdir("data")
    tp, fp, fn, tn = np.zeros(20), np.zeros(20), np.zeros(20), np.zeros(20)
    start, end, step = 0, 10, 10
    while end < 101:
        test_files = files[start:end]

        classifier = bc.BayesClassifier((start, end))
        for file in test_files:
            class_attitudes = classifier.count_file_class(file)
            for h in range(4, 8):
                cls = 1 if class_attitudes >= float(h) / 10 else 2
                # is_spam = " spam " if cls == 2 else " not spam "
                # print(file + " is " + is_spam)
                if "legit" in file and cls == 1:
                    tp[h] += 1
                elif "legit" in file and cls == 2:
                    tn[h] += 1
                elif "legit" not in file and cls == 1:
                    fp[h] += 1
                elif "legit" not in file and cls == 2:
                    fn[h] += 1

        # for h in range(0, 20):
        #     print("h = " + str(float(h) / 10))
        #     print("So We've got " + str(tp[h]+fn[h]) + " guesses accuracy is " + str((tp[h]+fn[h])/(tp[h]+fn[h]+fp[h]+tn[h])))

        start += step
        end += step

    for h in range(4, 8):
        p = tp[h] / (tp[h] + fp[h])
        r = tp[h] / (tp[h] + fn[h])
        print("Final f-measure is " + str(2 * p * r / (r + p)))

if __name__ == "__main__":
    main()