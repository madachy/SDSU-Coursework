'''
Created on Apr 15, 2018

@author: mroch
'''

from copy import deepcopy
from random import shuffle

from ml_lib.learning import (DataSet, DecisionTreeLearner, NeuralNetLearner)
from ml_lib.utils import print_table
from std_cv import cross_validation


def shuffle_data(dataset: DataSet):
    shuffle(dataset.examples)


def learn(dataset: DataSet) -> dict:
    data = deepcopy(dataset)
    shuffle_data(data)

    return_value = dict()

    return_value[DecisionTreeLearner] = cross_validation(DecisionTreeLearner, data)
    # Neural Net Needs the Numbers like the Cookie Monster needs Cookies
    data.classes_to_numbers()
    data.attributes_to_numbers()
    return_value[NeuralNetLearner] = cross_validation(NeuralNetLearner, data)

    return return_value


def main():
    datasets = [DataSet(name="iris"), DataSet(name="orings"), DataSet(name="zoo"), DataSet(name="restaurant")]
    # Abalone completes, but will take a while
    # datasets.append(DataSet(name="abalone"))

    header = ["Dataset   ",
              "Solve Method        ",
              "mean(fold_errV)     ",
              "stdev(fold_errV)    ",
              "fold_errV                                           "]

    rows = list()

    # Header Separator
    rows.append(['-' * (len(header[i]) + 1) for i in range(len(header))])

    for dataset in datasets:
        result = learn(dataset)

        for key in result.keys():
            row = list()
            row.append(dataset.name)
            row.append(key.__name__)
            for v in result[key]:
                row.append(v)

            rows.append(row)

    print_table(rows, header=header, sep="\t| ")


if __name__ == '__main__':
    main()
