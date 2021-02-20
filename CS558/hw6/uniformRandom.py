from numpy import random
from numpy import cumsum
import matplotlib.pyplot as plt
from collections import Counter


def main():
    input_lines = list()
    with open("uniformRandom.csv") as input_file:
        for line in input_file:
            input_lines.append(line.split(','))
    low = int(input_lines[1][0])
    high = int(input_lines[1][1])
    n = int(input_lines[1][2])
    sensitivity = int(input_lines[1][3])
    random_variates = [round(i, sensitivity) for i in random.uniform(low, high, n)]
    variate_counts = Counter(random_variates)
    variates = list()
    probability = list()
    for variate in sorted(variate_counts.items(), key=lambda tup: tup[0]):
        variates.append(variate[0])
        probability.append(variate[1] / n)
    probability_cdf = cumsum(probability)
    print(variate_counts)
    d_plus = max([(i + 1) / n - probability_cdf[i] for i in range(len(probability_cdf))])
    d_minus = max([probability_cdf[i] - i / n for i in range(len(probability_cdf))])
    d = max(d_plus, d_minus)
    plt.plot(variates, probability, label="PDF")
    plt.plot(variates, probability_cdf, c="red", label="CDF")
    plt.plot([i for i in range(low, (high + 1))], [i / (high - low) for i in range(high - low + 1)], c="green",
             label="True CDF")
    plt.title("Random Values between {} and {} for size {} at rounding {}, D: {:.4f}".format(low, high, n, sensitivity, d))
    plt.xlabel("X")
    plt.ylabel("f(x) or F(X)")
    plt.legend()
    plt.show()
    if n > 40:
        numerators = [1.22, 1.36, 1.51, 1.63]
        print("N:{} -> Alpha:D 0.1:{:.4f} 0.05:{:.4f} 0.02:{:.4f} 0.01:{:.4f}".format(n, *[numerator / (n ** 0.5) for numerator in
                                                                           numerators]))


if __name__ == '__main__':
    main()
