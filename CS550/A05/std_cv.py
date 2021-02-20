from statistics import (stdev, mean)
from ml_lib.learning import (err_ratio, train_and_test)


def cross_validation(learner, dataset, k=10):
    """Perform k-fold cross_validation
    Run k trials where each trial has a different (k-1)/k percentage
    of the data as training data and 1/k as test data.
    
    Returns tuple (mean_err, std_err, fold_errors, models)
    """

    fold_errV = list()  # fold error on validation data

    n = len(dataset.examples)
    examples = dataset.examples

    for fold in range(k):  # for each fold
        # Split into train and test
        # Note that this is not a canonical cross validation where
        # every pieces of data is used for training and testing
        # due to the shuffling above.
        train_data, val_data = train_and_test(dataset, fold * (n / k),
                                              (fold + 1) * (n / k))

        dataset.examples = train_data
        h = learner(dataset)

        # predict and accumulate the error rate on validation data
        fold_errV.append(err_ratio(h, dataset, val_data))
        # Reverting back to original once test is completed
        dataset.examples = examples

    # Return average per fold rates for validation data
    return mean(fold_errV), stdev(fold_errV), fold_errV
