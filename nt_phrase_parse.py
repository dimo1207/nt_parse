"""This module loads a pickled dictionary containing the NRSV
New Testament, and then searches each chapter of each book
for the user-entered phrase or word.
If found, the function returns the book title and
the chapter in which the phrase/word was found."""

import pickle


def nt_phrase_parse():
    """This is the sole function of the module."""
    nt_dict = pickle.load(open("nt_dict", "rb"))
    phrase = input("What word or phrase are you looking for?\n")
    total_count = 0

    for key in nt_dict.keys():
        for i in nt_dict[key]:
            if phrase in nt_dict[key][i]:
                print(key, i)
                total_count += nt_dict[key][i].count(phrase)

    print("\nThis phrase occurs", total_count, "times in the New Testament.\n")


if __name__ == '__main__':
    nt_phrase_parse()
