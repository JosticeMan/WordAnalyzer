"""
Computer Science AP/X Zipf's Law
CSCI-140/242
Project 1

Generates and plots the relative popularity of each word, in relation to
all others, across all occurrences and all years.

Author: Justin Yau
"""


import argparse                     # ArgumentParser
import sys                          # stderr
import matplotlib.pyplot as plt     # loglog, plot, annotate, title, xlabel, ylabel, show
from typing import List
from typing import Tuple
from operator import itemgetter


def read_words(path: str) -> dict:
    """
    Read word entries from a file into a dictionary.
    :param path: The name of the file
    :return: A dictionary with words and the total number of occurrences based on the inputted file
    """
    try:
        dictionary = {}
        f = open(path)
        for line in f:
            fields = line.split(", ")
            if fields[0] in dictionary:
                dictionary[fields[0]] += int(fields[2])
            else:
                dictionary[fields[0]] = int(fields[2])
        return dictionary
    except FileNotFoundError:
        sys.stderr.write("Error: " + path + " does not exist!")
        exit()


def determine_rank(target: str, ranks: List[Tuple], filename: str) -> int:
    """
    Determines the rank of the inputted word based on the rank list
    :param target: The word to find the rank of
    :param ranks: A list with all the words and their respective ranks
    :param filename: The name of the file the ranks were extracted from
    :return: The rank of the inputted word
    """
    ranked_word_list = [rank[0] for rank in ranks]
    for i, j in enumerate(ranked_word_list):
        if j == target:
            print(target + " is ranked #" + str(i + 1))
            return i + 1
    sys.stderr.write("Error: " + target + " does not appear in " + filename + "!")
    exit()


def print_first_few(num: int, ranks: List[Tuple]) -> None:
    """
    Prints the first x amount of top words and their frequency
    :param num: The number of highest ranked words to print
    :param ranks: A list containing all the words and their ranks
    :return: Nothing
    """
    for i, rank in enumerate(ranks[:num]):
        print("#" + str(i + 1) + ": " + str(rank[0]) + " -> " + str(rank[1]))


def plot_occurrences(ranks: List[Tuple], word: str, rank: int, wordy: int, filename: str) -> None:
    """
    Plots a loglog graph based on the inputted information
    :param ranks: A list containining all the words and their ranks
    :param word: The word to find the rank of
    :param rank: The rank of the word to find the rank of
    :param wordy: The occurrences of the word to find the rank of
    :param filename: The file we extracted the ranks from
    :return: Nothing
    """
    x_data = range(1, len(ranks) + 1)
    y_data = [rank[1] for rank in ranks]
    plt.loglog(x_data, y_data)
    plt.plot(rank, wordy, color='red', marker="*", markeredgecolor='black', markersize="10")
    plt.annotate(word, xy=(rank, wordy * 1.05))
    plt.title("Word Frequencies: " + filename)
    plt.ylabel("Total number of occurrences")
    plt.xlabel('Rank of word("' + word + '" is rank #' + str(rank) + ")")
    plt.show()


def main():
    """
    Processes the arguments and calls the appropriate functions based on them
    :return: Nothing
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=int, help="Display the top OUTPUT (#) ranked words by number of "
                                                         "occurrences.")
    parser.add_argument("-p", "--plot", help="Plot the word rankings from top to bottom based on "
                                             "occurrences", action="store_true")
    parser.add_argument("word", help="A word to display the overall ranking of")
    parser.add_argument("filename", help="A comma separated value unigram file")
    args = parser.parse_args()
    # print("Reading File...")
    dictionary = read_words(args.filename)
    # print("Done Reading File...")
    # print("Processing")
    ranked_list = sorted(dictionary.items(), key=itemgetter(1), reverse=True)
    rank = determine_rank(args.word, ranked_list, args.filename)
    if args.output > 0 or args.plot:
        if args.output > 0:
            print_first_few(args.output, ranked_list)
        if args.plot:
            plot_occurrences(ranked_list, args.word, rank, dictionary[args.word], args.filename)


if __name__ == '__main__':
    main()