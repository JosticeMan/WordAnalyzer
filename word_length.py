"""
Computer Science AP/X Zipf's Law
CSCI-140/242
Project 1

Generates and plots the average word length over a range of years.

Author: Justin Yau
"""


import argparse                     # ArgumentParser
import sys                          # stderr
import matplotlib.pyplot as plt     # plot, xlabel, ylabel, xticks, title, show
from operator import itemgetter
from typing import List
from typing import Tuple


def read_words(path: str, start: int, end: int) -> dict:
    """
    Read word entries from a file into a dictionary.
    :param path: The name of the file
    :param start: The first year to filter
    :param end: The last year to filter
    :return: A dictionary with words and the total number of occurrences based on the inputted file
    """
    try:
        dictionary = {}
        with open(path) as f:
            for line in f:
                fields = line.split(", ")
                if start <= fields[1] <= end:
                    word_length = int((len(fields[0]) * int(fields[2])))
                    if fields[1] in dictionary:
                        dictionary[fields[1]][1] += int(fields[2])
                        dictionary[fields[1]][0] += word_length
                    else:
                        dictionary[fields[1]] = [word_length, int(fields[2])]
        return dictionary
    except FileNotFoundError:
        sys.stderr.write("Error: " + path + " does not exist!")
        exit()


def print_entries(data: List[Tuple]) -> None:
    """
    Prints the year and average word length on separate lines
    :param data: A list of tuples containing years and average word lengths
    :return: Nothing
    """
    for item in data:
        print(str(item[0]) + ": " + str(item[1]))


def average_length(data: dict) -> dict:
    """
    Creates or Calculates a new dictionary with years and their average word lengths
    :param data: A dictionary containing years and the word lengths
    :return: A dictionary with years and their average word lengths
    """
    dictionary = {}
    for key in data.items():
        dictionary[key[0]] = int(key[1][0])/int((key[1][1]))
    return dictionary


def plot_lengths(data: List[Tuple], start: int, end: int, filename: str) -> None:
    """
    Plots word length data onto a coordinate plane and connects them.
    :param data: The data to be plotted
    :param start: The starting year for the data
    :param end: The ending year for the data
    :param filename: The file where the data was extracted from
    :return: Nothing
    """
    y_data = [length[1] for length in data]
    x_data = [length[0] for length in data]
    plt.plot(x_data, y_data)
    plt.xlabel("Year")
    plt.ylabel("Average Word Length")
    plt.title("Average Word Length from " + str(start) + " to " + str(end) + ": " + filename)
    plt.xticks(x_data[::int(((int(start) - int(end))/5))])
    plt.show()


def main():
    """
        Handles inputted argument and calls functions based on those arguments
        :return: Nothing
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Display the average word lengths over years", action="store_true")
    parser.add_argument("-p", "--plot", help="Plot the average word lengths over years", action="store_true")
    parser.add_argument("start", help="The starting year range")
    parser.add_argument("end", help="The ending year range")
    parser.add_argument("filename", help="A comma separated value unigram file")
    args = parser.parse_args()
    if args.start > args.end:
        sys.stderr.write("Error: Start year must be less than or equal to end year!")
        exit()
    if args.output or args.plot:
        dictionary = read_words(args.filename, args.start, args.end)
        average = average_length(dictionary)
        sorted_list = sorted(average.items(), key=itemgetter(0))
        if args.output:
            print_entries(sorted_list)
        if args.plot:
            plot_lengths(sorted_list, args.start, args.end, args.filename)


if __name__ == '__main__':
    main()