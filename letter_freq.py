"""
Computer Science AP/X Zipf's Law
CSCI-140/242
Project 1

Generates and plots the frequency distribution of individual letters
in the words across all occurrences and all years.

Author: Justin Yau
"""

import argparse                     # ArgumentParser
import word_freq                   # read_words
import numpy as np                  # arange
import sys                          # maxsize
import matplotlib.pyplot as plt     # bar, title, ylabel, xlabel, xticks, yticks, show
from word_count import Word
from typing import List

# Constant to reduce time spent generating a list of the letters in the alphabet
ALPHABET = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
            "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")


def calculate_frequencies(data: List[Word]) -> dict:
    """
    Retrieves the letter count and calculates the frequency based on the retrieved information
    :param data: The data with words and their count in a specific year
    :return: A dictionary with all the letter counts
    """
    frequencies = initialize_dictionary()
    count = determine_count(data)
    for letter in ALPHABET:
        frequencies[letter] = count[letter]/count["sum"]
    return frequencies


def print_frequencies(data: dict) -> None:
    """
    Prints out all the letters of the alphabet and their frequencies
    :param data: A dictionary containing the letters of the alphabet and their frequencies
    :return: Nothing
    """
    for letter in ALPHABET:
        print(letter + ": " + str(data[letter]))


def highest_frequency(data: List[int]) -> int:
    """
    Determines the highest frequency in the given data set
    :param data: The data to be searched
    :return: The highest frequency in the given data set
    """
    highest = -sys.maxsize - 1
    for num in data:
        if num > highest:
            highest = num
    return highest


def plot_frequencies(data: dict, title: str) -> None:
    """
    Plots the frequencies in a bar graph format with the given title
    :param data: The data to be plotted
    :param title: The name of the to be plotted bar graph
    :return: Nothing
    """
    ind = np.arange(len(ALPHABET))
    width = .5
    x_data = []
    for letter in ALPHABET:
        x_data.append(data[letter])
    plt.bar(ind, x_data, width)
    plt.title("Letter Frequencies: " + title)
    plt.ylabel("Frequency")
    plt.xlabel("Letters")
    plt.xticks(ind, ALPHABET)
    plt.yticks(np.arange(0, highest_frequency(x_data) + .05, 0.05))
    plt.show()


def determine_count(data: dict) -> dict:
    """
    FASTER VERSION
    Goes through the dictionary entries and determines the number of times each letter appears in the words
    :param data: The data to be searched
    :return: A dictionary with the number of times each letter appears in the words of the specified dictionary
    """
    count = initialize_dictionary()
    sum = 0
    for key, value in data.items():
        for letter in key:
            count[letter] += value
            sum += value
    count["sum"] = sum
    return count


def initialize_dictionary() -> dict:
    """
    Creates a dictionary with the letters of the alphabet having 0 associated with them
    :return: A dictionary with the letters of the alphabet having 0 associated with them
    """
    result = {}
    for letter in ALPHABET:
        result[letter] = 0
    return result


def main():
    """
    Handles inputted argument and calls functions based on those arguments
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Display letter frequencies to standard output", action="store_true")
    parser.add_argument("-p", "--plot", help="Plot letter frequencies using matplotlib", action="store_true")
    parser.add_argument("filename", help="A comma separated value unigram file")
    args = parser.parse_args()
    print("Reading File")
    dictionary = word_freq.read_words(args.filename)
    print("Done Reading File...")
    print("Processing...")
    if args.output or args.plot:
        frequencies = calculate_frequencies(dictionary)
        if args.output:
            print_frequencies(frequencies)
        if args.plot:
            plot_frequencies(frequencies, args.filename)


if __name__ == '__main__':
    main()
