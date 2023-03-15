import sys
import numpy as np
from describe import read_data
from sklearn.metrics import accuracy_score

class LRTrainer():

    def __init__(self):
        self.learning_rate = 0.001
        self.max_iterations = 1500
        self.weights = []

    def logistic_regression(self, X, y):

        """ Logistic regression algorithm """

        X = np.insert(X, 0, 1, axis=1)
        for house in np.unique(y):
            current_house_vs_all = np.where(y == house, 1, 0)
            w = np.ones(X.shape[1])
            for _ in range(self.max_iterations):
                output = np.dot(X, w)
                errors = current_house_vs_all - self._sigmoid_function(output)
                gradient = np.dot(X.T, errors)
                w += self.learning_rate * gradient
            self.weights.append((w, house))
        return (self.weights)
    
    def compute_score(self, X, y):
        return (accuracy_score(y, self.predict(X)) * 100)

    def predict(self, X):
        return ([self._predict_one(i) for i in np.insert(X, 0, 1, axis=1)])
    
    def _predict_one(self, grades):
        max_probability = (-10, 0)
        for weight, house in self.weights:
            if ((grades.dot(weight), house) > max_probability):
                max_probability = (grades.dot(weight), house)
        return (max_probability[1])

    def _sigmoid_function(self, X):
        return (1 / (1 + np.exp(-X)))

def normalize(column):
    mini = min(column)
    maxi = max(column)
    for index in range(len(column)):
        try:
            column[index] = ((column[index] - mini) / (maxi - mini))
        except ZeroDivisionError:
            print("\033[1;91mError: \033[0mA whole field of the dataset is equal, which makes no sense for this algorithm...")
            sys.exit(1)

def get_relevant_data(dataset):
    if (dataset['Hogwarts House'].isnull().sum() > 0):
        print("\033[1;91mError: \033[0mCannot train with selected dataset: House data is missing!")
        sys.exit(1)
    dataset = dataset.dropna()
    try:
        target = np.array(dataset["Hogwarts House"])
        features = np.array(dataset[["Herbology", "Defense Against the Dark Arts", "Ancient Runes", "Charms"]])
    except:
        print("\033[1;91mError: \033[0mMissing features from dataset!")
        sys.exit(1)
    return target, features

def main():
    if len(sys.argv) != 2:
        print("\033[1;91mError, do: python3 logreg_train.py [your dataset]")
        exit(1)
    dataset = read_data(sys.argv[1])
    arr = np.random.randint(0, 100, len(dataset)) > 10
    target, features = get_relevant_data(dataset[:][arr])
    np.apply_along_axis(normalize, 0, features)
    trainer = LRTrainer()
    weights = trainer.logistic_regression(features, target)
    try:
        np.save("weights", np.array(weights, dtype='object'))
    except:
        print("\033[1;91mError while saving weights value.")
        exit(1)
    print("Weights saved to weights.npy")
    target0, features0 = get_relevant_data(dataset[:][~arr])
    np.apply_along_axis(normalize, 0, features0)
    print("Precision: " + "{:.2f}".format(trainer.compute_score(features0, target0)) + "%")

if __name__ == "__main__":
    main()