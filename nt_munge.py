"""This module imports the chapter_tups function
from nt_most_cmn, and requires a parameter
specifying the desired text. The function defines
a mask of unwanted words, and then by indexing
leaves these words out of the final return value.
It also collects a list of hapaxes -- words
occuring only once in the text."""
import sys
import pickle
from most_common import most_common
sys.tracebacklimit = None


def munge():
    """This is the sole function of the module."""
    nt_dict = pickle.load(open("nt_dict", "rb"))
    text = input("Which book would you like to parse?\n").title()
    # Chapter index (-1 to adjust for indexing rules):
    idx = int(input("What chapter are you interested in?\n")) - 1
    # This code raises an error if the chapter entered is not in the book:
    if idx > len(nt_dict[text]) or idx <= -1:
        raise IndexError(
            "The book of {} has {} chapters. Please enter a number between {} and {}."
            .format(text, len(nt_dict[text]), 1, len(nt_dict[text])))

    chapter_tups = most_common(text)
    hapaxes = []
    # Masks of unwanted words:
    unwanted = ['is', 'to', 'of', 'and', 'in', 'with', 'are', 'this', 'for',
                'the', 'a', 'an', 'he', 'her', 'him', 'she', 'they', 'them', 'you',
                'we', 'i', 'have', 'his', 'who', 'were', 'whose', 'when', 'was',
                'said', 'from', 'whom', 'but', 'what', 'that', 'it', 'then', 'which',
                'where', 'here', 'me', 'those', 'by', 'even', 'so', 'about', 'though',
                'as', 'also']
    numbers = [str(x) for x in range(75)]

    for i, _ in enumerate(chapter_tups[idx]):
        while chapter_tups[idx][i][1] in unwanted or chapter_tups[idx][i][1] in numbers:
            del chapter_tups[idx][i]
            chapter_tups[idx].append("for deletion")
        while chapter_tups[idx][i][0] == 1:
            hapaxes.append(chapter_tups[idx][i][1])
            del chapter_tups[idx][i]
            chapter_tups[idx].append("for deletion")

    for i, _ in enumerate(hapaxes):
        while hapaxes[i] in unwanted or hapaxes[i] in numbers:
            del hapaxes[i]
            hapaxes.append("for deletion")

    # the following del statements index "for deletion" in each list,
    # and then delete each value following that index via slicing:
    del chapter_tups[idx][chapter_tups[idx].index("for deletion"):]
    del hapaxes[hapaxes.index("for deletion"):]

    print("\nMost commonly occurring words in the book of {}, Chapter {}:\n\n"
          .format(text, idx + 1), chapter_tups[idx])
    haps = input(
        "\nWould you also like to return a list of words occurring only once? (Y or N):\n")
    if haps == "Y" or haps == 'y':
        print("\nWords that occur only once:\n", hapaxes[::-1])


if __name__ == "__main__":
    munge()
