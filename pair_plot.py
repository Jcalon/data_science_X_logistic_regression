import sys
import matplotlib.pyplot as plt
from describe import read_data, clean_data
from histogram import fill_histogram
from scatter_plot import fill_scatter_plot
import itertools

def pair_plot(dataset, clean_dataset):
    fig = plt.figure(figsize=(25,15))
    i = 1
    size = len(clean_dataset.columns)
    for class_1, class_2 in itertools.product(clean_dataset.columns, clean_dataset.columns):
        ax = fig.add_subplot(size, size, i)
        if (i <= size):
                ax.set_title(class_2)
        if (i % size == 1):
                ax.set_ylabel(class_1[0:6])
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        if (class_1 != class_2):
            fill_scatter_plot(ax, dataset, class_1, class_2)
        else:
            fill_histogram(ax, dataset, class_1)
        i += 1
    if (len(clean_dataset.columns)):
        fig.tight_layout()
        plt.show()
    else:
        print("\033[1;91mError: \033[0mNo data to display in a scatter plot!")

def main():
    if len(sys.argv) != 2:
        print("\033[1;91mError, do: python3 pair_plot.py [your dataset]")
        exit(1)
    dataset = read_data(sys.argv[1])
    clean_dataset = clean_data(dataset)
    pair_plot(dataset, clean_dataset)

if __name__ == "__main__":
    main()