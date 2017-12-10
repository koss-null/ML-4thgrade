import NaiveBayes.bayesClassifier as bc
import os
import shutil


def main():
    files = os.listdir("data")
    tp, fp, fn, tn = 0, 0, 0, 0
    start, end = 0, 10
    while end < 101:
        test_files = files[start:end]

        classifier = bc.BayesClassifier((start, end))
        for file in test_files:
            cls = classifier.count_file_class(file)
            print(file + " is " + " spam " if cls == 0 else " not spam ")
            if "legit" in file and cls == 1:
                tp += 1
            elif "legit" in file and cls == 0:
                tn += 1
            elif "legit" not in file and cls == 1:
                fp += 1
            elif "legit" not in file and cls == 0:
                fn += 1

        print("So We've got " + str(tp+fn) + " guesses accuracy is " + str((tp+fn)/(tp+fn+fp+tn)))

        start += 10
        end += 10

    p = tp / (tp + fp)
    r = tp / (tp + fn)
    print("Final f-measure is " + str(2 * p * r / (r + p)))

if __name__ == "__main__":
    main()