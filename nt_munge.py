"""This module imports the chapter_tups function
from nt_most_cmn, and requires a parameter
specifying the desired text. The function defines
a mask of unwanted words, and then by indexing
leaves these words out of the final return value.
It also collects a list of hapaxes -- words
occuring only once in the text."""

from nt_most_cmn import nt_most_cmn


def munge():
    """This is the sole function of the module."""
    chapter_tups = nt_most_cmn()
    hapaxes = []
    idx = -1  # Chapter index
    # Mask of unwanted words:
    unwanted = ['is', 'to', 'of', 'and', 'in', 'with', 'are', 'this',
                'the', 'a', 'an', 'he', 'her', 'him', 'she', 'they', 'them', 'you',
                'we', 'i', 'have', 'his', 'who', 'were', 'whose', 'when', 'was',
                'said', 'from', 'whom', 'but', 'what', 'that', 'it', 'then', 'which',
                'where', 'here', 'me', 'those', 'by', 'even', 'so', 'about', 'though',
                'as', 'also']

    for i in range(len(chapter_tups[idx])):
        while chapter_tups[idx][i][1] in unwanted:
            del chapter_tups[idx][i]
            chapter_tups[idx].append("for deletion")
        while chapter_tups[idx][i][0] == 1:
            hapaxes.append(chapter_tups[idx][i])
            del chapter_tups[idx][i]
            chapter_tups[idx].append("for deletion")

    del_idx = chapter_tups[idx].index("for deletion")
    print(chapter_tups[idx][:del_idx])
    # print(hapaxes)


munge()
