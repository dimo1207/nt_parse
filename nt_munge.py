"""This module imports the chapter_tups function
from nt_most_cmn, and requires a parameter
specifying the desired text. The function defines
a mask of unwanted words, and then by indexing
leaves these words out of the final return value.
It also collects a list of hapaxes -- words
occuring only once in the text."""

from most_common import *


def munge():
    """This is the sole function of the module."""
    text = input("Which book would you like to parse?\n")
    if not text.istitle():
        text = text.title()
    idx = int(input("What chapter are you interested in?\n"))  # Chapter index

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

    for i in range(len(chapter_tups[idx])):
        while chapter_tups[idx][i][1] in unwanted or chapter_tups[idx][i][1] in numbers:
            del chapter_tups[idx][i]
            chapter_tups[idx].append("for deletion")
        while chapter_tups[idx][i][0] == 1:
            hapaxes.append(chapter_tups[idx][i])
            del chapter_tups[idx][i]
            chapter_tups[idx].append("for deletion")

    del_idx = chapter_tups[idx].index("for deletion")
    del chapter_tups[idx][del_idx:]

    for i in range(len(hapaxes)):
        while hapaxes[i][1] in unwanted or hapaxes[i][1] in numbers:
            del hapaxes[i]
            hapaxes.append("for deletion")

    del_hap = hapaxes.index("for deletion")
    del hapaxes[del_hap:]

    print("\nMost commonly occurring words in the book of {}, Chapter {}:\n\n"
            .format(text, idx), chapter_tups[idx])
    
    haps = input(
        "\nWould you also like to return a list of words occurring only once? (Y or N):\n")
    if haps == "Y" or haps == 'y':
        print("\nWords that occur only once:\n")
        clear_read = [tup[1] for tup in hapaxes]
        print(clear_read[::-1])


if __name__ == "__main__":
    munge()
