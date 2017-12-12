import NaiveBayes.bayesClassifier as bc
import os
import numpy as np
import shutil


def main():
    files = os.listdir("data")
    tp, fp, fn, tn = np.zeros(140), np.zeros(140), np.zeros(140), np.zeros(140)
    start, end, step = 0, 20, 20
    while end < 101:
        print(end)
        test_files = files[start:end]

        classifier = bc.BayesClassifier((start, end))
        for file in test_files:
            class_attitudes = classifier.count_file_class(file)
            for h in range(80, 120):
                cls = 1 if (class_attitudes >= (float(h) / 100)) else 2
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

    for h in range(80, 120):
        print(tp[h])
        print(tn[h])
        print(fp[h])
        print(fn[h])

    for h in range(80, 120):
        p = tp[h] / (tp[h] + fp[h])
        r = tp[h] / (tp[h] + fn[h])
        print("h is " + str(float(h) / 100))
        print("precision:" + str(p) + " recall: " + str(r))
        print("      positive|negative")
        print("true:     " + str(tp[h]) + " |   " + str(tn[h]))
        print("false:    " + str(fp[h]) + " |   " + str(fn[h]))
        print("Final f-measure is " + str(2 * p * r / (r + p)))

if __name__ == "__main__":
    main()