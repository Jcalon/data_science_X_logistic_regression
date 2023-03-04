import sys
import csv
import numpy as np
import pandas as pd
from describe import read_data
from logreg_train import normalize

class LRPredictor():

    def __init__(self):
        pass

    def predict(self, X, weights):
        return ([self._predict_one(i, weights) for i in np.insert(X, 0, 1, axis=1)])

    def _predict_one(self, grades, weights):
        max_probability = (-10, 0)
        for weight, house in weights:
            if ((grades.dot(weight), house) > max_probability):
                max_probability = (grades.dot(weight), house)
        return (max_probability[1])

def get_weights(file):
    try:
        weights = np.load(file, allow_pickle=True)
    except:
        print("\033[1;93mWarning: \033[0mCheck that csv file containing the weights exists and you have appropriate access rights.")
        print("You should use logreg_train.py first.")
        print("Defaulting to Null weights for everything.")
        weights = []
        for house in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            weights.append(([0, 0, 0, 0, 0], house))
    return weights

def get_relevant_data(dataset):
    pd.options.mode.chained_assignment = None
    used_features = dataset[["Herbology", "Defense Against the Dark Arts", "Ancient Runes", "Charms"]]
    for column in used_features:
        used_features[column] = used_features[column].fillna(used_features[column].mean())
    features = np.array(used_features)
    return features

def main():
    if len(sys.argv) != 2:
        print("\033[1;91mError, do: python3 logreg_predict.py [dataset_test]")
        exit(1)
    dataset = read_data(sys.argv[1])
    weights = get_weights('weights.npy')
    features = get_relevant_data(dataset)
    np.apply_along_axis(normalize, 0, features)
    predictor = LRPredictor()
    houses = predictor.predict(features, weights)
    with open('houses.csv', 'w') as csvfile:
        file = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        file.writerow(["Index","Hogwarts House"])
        i = 0
        for row in houses:
            file.writerow([i, row])
            i += 1
    print("Resulting houses saved in houses.csv")

if __name__ == "__main__":
    main()