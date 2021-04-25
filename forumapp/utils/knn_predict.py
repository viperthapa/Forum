import math
from collections import Counter

import numpy as np


def distance_of_eucildian(x1, x2):
    return np.sqrt(np.sum(np.square(x1 - x2)))

def mean_of_labels(labels):
    return sum(labels) / len(labels)

def mode_of_labels(labels):
    return Counter(labels).most_common(1)[0][0]

class KNNClassifier:
    def __init__(self, k=5, voting_option = mode):
        self.K = k
        self.voting_option = voting_option

    def fit(self, X, y):
        self.X = X
        self.y = y

    def predict(self, X_test):
        assert self.K <= len(self.X), "Expected: k less than sample size"

        predictions = []
        distances = []
        # 1. Iterate over all test data
        for i in range(len(X_test)):

            distances = np.array(np.sqrt(np.sum(np.square(self.X - X_test[i]), axis=1)))
#             distances = np.array([euclidean_distance(X_t, X_test[i]) for X_t in self.X])

            sorted_distances_index = distances.argsort()[:self.K]

            k_nearest_labels = [self.y[index] for index in sorted_distances_index]
            predictions.append(self.voting_option(k_nearest_labels))


        predictions = np.array(predictions)

        return predictions
