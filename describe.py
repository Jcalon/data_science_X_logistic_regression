import pandas as pd
import sys
import numpy as np
import math

def read_data(file):
    try:
        dataset = pd.read_csv(file, index_col = "Index")
    except IOError:
        print("\033[1;91mError: \033[0mCheck that csv dataset file exists and you have appropriate access rights.")
        sys.exit(1)
    except (pd.errors.ParserError, pd.errors.EmptyDataError) as err:
        print("\033[1;91mError: \033[0mThe csv file contains corrupted data. Following is the error message from pandas:\n", err)
        sys.exit(1)
    return (dataset)

def clean_data(dataset):
    clean_dataset = dataset
    for column in clean_dataset.columns:
        try:
            float(clean_dataset[column][0])
        except ValueError:
            clean_dataset = clean_dataset.drop([column], axis=1)
    clean_dataset = clean_dataset.dropna(axis=1, how='all')
    return (clean_dataset)

def standard_deviation(column, count, mean):
    std = 0
    for value in column:
        if not np.isnan(value):
            std += (value - mean) ** 2
        else:
            continue
    std /= count
    return np.sqrt(std)

def describe_data(dataset):
    describe_dataset = pd.DataFrame(index = ["Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"], columns=dataset.columns)
    for column in dataset.columns:
        count = 0
        mean = 0
        tab = []
        for value in dataset[column]:
            if not np.isnan(value):
                count += 1
                mean += value
                tab.append(value)
            else:
                continue
        mean /= count
        describe_dataset[column]["Count"] = count
        describe_dataset[column]["Mean"] = mean
        describe_dataset[column]["Std"] = standard_deviation(dataset[column], count, mean)
        tab.sort()
        describe_dataset[column]["Max"] = tab[count - 1]
        describe_dataset[column]["Min"] = tab[0]
        describe_dataset[column]["25%"] = tab[math.ceil(count / 4) - 1]
        describe_dataset[column]["50%"] = tab[math.ceil((count + 1) / 2) - 1]
        describe_dataset[column]["75%"] = tab[math.ceil(3 * count / 4) - 1]
    describe_dataset.rename(columns=lambda c: c[:14], inplace=True)
    return describe_dataset

def main():
    if len(sys.argv) != 2:
        print("\033[1;91mError, do: python3 describe.py [your dataset]")
        exit(1)
    dataset = read_data(sys.argv[1])
    clean_dataset = clean_data(dataset)
    describe_dataset = describe_data(clean_dataset)
    print('\n')
    if (not dataset.empty):
        print(describe_dataset)
    else:
        print("No data!")

if __name__ == "__main__":
    main()