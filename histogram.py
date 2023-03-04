import sys
import matplotlib.pyplot as plt
from describe import read_data, clean_data

def fill_histogram(ax, dataset, requested_class):
    ax.hist(dataset[dataset['Hogwarts House'] == "Gryffindor"][requested_class], alpha=0.5, color='#B92100', label="Gryffindor")
    ax.hist(dataset[dataset['Hogwarts House'] == "Hufflepuff"][requested_class], alpha=0.5, color='#e8c227', label="Hufflepuff")
    ax.hist(dataset[dataset['Hogwarts House'] == "Ravenclaw"][requested_class], alpha=0.4, color='#6693fc', label="Ravenclaw")
    ax.hist(dataset[dataset['Hogwarts House'] == "Slytherin"][requested_class], alpha=0.4, color='#008700', label="Slytherin")
    if (dataset['Hogwarts House'].isnull().sum() > 0):
        ax.hist(dataset[requested_class], alpha=0.7, color='black', label="Ghost")

def plot_histograms(dataset, clean_dataset):
    fig = plt.figure(figsize=(25,15))
    fig.suptitle("Grade repartition per House for each class", y=0.15)
    i = 1
    for column in clean_dataset.columns:
        ax = fig.add_subplot(4, 4, i)
        ax.set_title(column)
        fill_histogram(ax, dataset, column)
        i += 1
    if (len(clean_dataset.columns)):
        handles, labels = ax.get_legend_handles_labels()
        fig.tight_layout(h_pad=2.1)
        fig.legend(handles, labels, loc="lower center")
        plt.show()
    else:
        print("\033[1;91mError: \033[0mNo data to display in a histogram!")
    

def main():
    if len(sys.argv) != 2:
        print("\033[1;91mError, do: python3 histogram.py [your dataset]")
        exit(1)
    dataset = read_data(sys.argv[1])
    clean_dataset = clean_data(dataset)
    plot_histograms(dataset, clean_dataset)

if __name__ == "__main__":
    main()