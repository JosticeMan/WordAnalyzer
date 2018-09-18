"""
Computer Science AP/X Zipf's Law
CSCI-140/242
Project 1

Counts the total number of occurrences of a word across all years.

Author: Justin Yaup
"""

import argparse         # ArgumentParser
import collections      # namedtuple
import sys              # path
from typing import List

"""
Word:
    Name (str): One unique word
    Year (int): Year the words appeared in
    Count (int): The number of times the word appeared in the aforementioned year
"""
Word = collections.namedtuple('Word', ('Name', 'Year', 'Count'))


def read_words(path: str) -> List[Word]:
    """
    Read word entries from a file into a list of Word namedtuples.
    :param path: The name of the file
    :return: A list of Words
    """
    try:
        dictionary = list()
        f = open(path)
        for line in f:
            fields = line.split(", ")
            dictionary.append(Word(fields[0], int(fields[1]), int(fields[2])))
        return dictionary
    except FileNotFoundError:
        sys.stderr.write("Error: " + path + " does not exist!")
        exit()


def find_word(data: List[Word], target: str) -> int:
    """
    Looks through the dictionary for the target word and adds together all the counts in their unique years
    :param data: The data to look through
    :param target: The word to total up the counts for
    :return: The total number of appearances the target word makes throughout the data's years
    """
    sum = 0
    for entry in [[word.Count] for word in data if word.Name == target]:
        sum += entry[0]
    if sum == 0:
        sys.stderr.write("Error: " + target + " does not appear!")
        exit()
    return sum


def main():
    """
    Specifies the arguments and calls the functions to determine the number of times a word appears in a data file
    :return: Nothing
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("word", help="A word to display the total occurrences of")
    parser.add_argument("filename", help="A comma separated value unigram file")
    args = parser.parse_args()
    print("Reading File")
    dictionary = read_words(args.filename)
    print("Done Reading File...")
    print(args.word + ": " + str(find_word(dictionary, args.word)))


if __name__ == '__main__':
    main()


