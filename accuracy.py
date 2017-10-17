#          true | false
# positive| 2   |  -2
# negative| 1   |   -1


def f_measure(errors):
    tp = sum(1. for a in errors if a == 2)
    fp = sum(1. for a in errors if a == -2)
    fn = sum(1. for a in errors if a == -1)

    print (tp, fp, fn)
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    # we are counting balanced F-measure, so alpha=0.5
    return 2 * precision * recall / (precision + recall)
