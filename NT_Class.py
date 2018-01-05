"""This module is composed of a class which contains
all of the individual functions I have designed to
parse the New Testament in various ways. These functions
are:
nt_most_cmn(text)
nt_parse(text, key_word)
nt_munge(chapter_tups) # requires output from nt_most_cmn(text)
nt_phrase_parse(phrase)
Dependency: pickle module"""


import pickle


class NewTestamentParse(object):
    """This class supports the following functions:
    nt_most_cmn(text)
    nt_parse(text, key_word)
    nt_munge(chapter_tups)  # requires output from nt_most_cmn(text)
    nt_phrase_parse(phrase)"""

    # def __init__(self):
    #     self.text = text
    #     self.phrase = phrase

    def nt_most_cmn(self, text):
        """This function prints out tuples of the most common words
        found in the user-entered book. The first value in the tuple
        is the frequency of the word, followed by the word itself.
        Only words occurring X or more times are printed."""

        with open("New Testament/" + text + ".txt") as book:
            chapters = [chp.split() for chp in book]

        count, words, chapter_list, chapter_tups = [], [], [], []
        chapter_count = 0

        for chapter in chapters:
            chapter_count += 1
            chapter_list.append(chapter_count)
            # List comprehension strips words of punctuation/case
            # and nests them in "words" list, organized by chapter:
            words.append([word.strip("();:\"\'?!,.").lower()
                          for word in chapter])

        for chapter in words:
            # Creates a list of nested lists containing word lengths;
            # corresponds to nested "words" lists:
            count.append([chapter.count(word) for word in chapter])

        for i in range(len(chapter_list)):
            chapter_tups.append(sorted(
                # Set comprehension producing (int, str) tuples from count/words lists:
                {(count, word) for count, word in zip(count[i], words[i])},
                reverse=True))  # Sorts the final list of sets in descending order by count.
        return chapter_tups

    def nt_parse(self, text, key_word):
        """This code iterates through New Testament text to find
        user-entered word, submitted on the command line.
        This version only finds the number of user-words per
        chapter, sites the chapter where the word occurs most
        frequently, and calculates the total occurence of this
        word in the book as a whole."""

        with open("New Testament/" + text + ".txt") as book:
            total_word_count = 0
            chp_count = 0
            max_chp = 0
            words_in_chapter = []
            for chapter in book:
                chp_count += 1
                word_count = 0
                if key_word in chapter:
                    word_count += chapter.count(key_word)
                words_in_chapter.append(word_count)
                print("Occurence of \"{}\" in Chapter {}: ".format
                      (key_word, chp_count), word_count)
                total_word_count += word_count
                most_freq = max(words_in_chapter)
            for cnt in words_in_chapter:
                if total_word_count == 0:
                    max_chp = "n/a"
                elif words_in_chapter.count(most_freq) > 1:
                    max_chp = []
                    for i, word in enumerate(words_in_chapter):
                        if word == most_freq:
                            max_chp.append(i + 1)
                elif cnt == max(words_in_chapter):
                    max_chp = (words_in_chapter.index(cnt) + 1)
            return print("\nTotal times that the word \"{}\" occurs in {}: "
                         .format(key_word, text), total_word_count,
                         "\nChapter where \"{}\" occurs most frequently: ".format
                         (key_word), max_chp)

    def munge(self, chapter_tups):
        """This module requires the chapter_tups output
        from nt_most_cmn. The function defines
        a mask of unwanted words, and then by indexing
        leaves these words out of the final return value.
        It also collects a list of hapaxes -- words
        occuring only once in the text."""
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
        return chapter_tups[idx][:del_idx]

    def nt_phrase_parse(self, phrase):
        """This module loads a pickled dictionary containing the NRSV
        New Testament, and then searches each chapter of each book
        for the user-entered phrase or word.
        If found, the function returns the book title and
        the chapter in which the phrase/word was found."""
        nt_dict = pickle.load(open("nt_dict", "rb"))

        for key in nt_dict.keys():
            for i in nt_dict[key]:
                if phrase in nt_dict[key][i]:
                    print(key, i)
        
