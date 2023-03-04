import sys
import matplotlib.pyplot as plt
from describe import read_data, clean_data

def fill_scatter_plot(ax, dataset, class_1, class_2):
    houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
    colors = ["#B92100", "#e8c227", "#6693fc", "#008700"]
    for house, color in zip(houses, colors):
        ax.scatter(dataset[dataset["Hogwarts House"] == house][class_1], dataset[dataset["Hogwarts House"] == house][class_2], color=color, alpha=0.1)
    if (dataset['Hogwarts House'].isnull().sum() > 0):
        ax.scatter(dataset[class_1], dataset[class_2], alpha=0.7, color='black')


def scatter_plot(dataset, clean_dataset):
    fig = plt.figure(figsize=(25,15))
    i = 1
    size = len(clean_dataset.columns)
    for class_1 in clean_dataset.columns:
        for class_2 in clean_dataset.columns:
            ax = fig.add_subplot(size, size, i)
            if (i <= size):
                 ax.set_title(class_2)
            if (i % size == 1):
                 ax.set_ylabel(class_1[0:6])
            ax.set_yticklabels([])
            ax.set_xticklabels([])
            fill_scatter_plot(ax, dataset, class_1, class_2)
            i += 1
    if (len(clean_dataset.columns)):
        fig.tight_layout()
        plt.show()
    else:
        print("\033[1;91mError: \033[0mNo data to display in a scatter plot!")

def main():
    if len(sys.argv) != 2:
        print("\033[1;91mError, do: python3 scatter_plot.py [your dataset]")
        exit(1)
    dataset = read_data(sys.argv[1])
    clean_dataset = clean_data(dataset)
    scatter_plot(dataset, clean_dataset)

if __name__ == "__main__":
    main()