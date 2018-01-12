"""This module is composed of a class which contains
all of the individual functions I have designed to
parse the New Testament in various ways. These functions
are:
full_parse()
book_parse()
most_common()
Dependency: pickle module"""
import pickle


class NewTestamentParse(object):
    """This class includes the following methods:
    full_parse()
    book_parse()
    most_common()
    """

    def __init__(self,
                 text,
                 phrase,
                 key_word="Default"):
        self.text = text
        self.phrase = phrase
        self.key_word = key_word
        if self.key_word == "Default":
            # length_of_words creates a list of word lengths from phrase:
            length_of_words = [(len(word)) for word in phrase.split()]
            idx = length_of_words.index(max(length_of_words))  # indexes longest word
            self.key_word = phrase.split()[idx] if len(phrase.split()) > 1 else phrase
            # ternary operator ; covers single word entries


    def full_parse(self):
        """This method loads a pickled dictionary containing the NRSV
        New Testament, and then searches each chapter of each book
        for the user-entered phrase or word.
        If found, the method returns the book title and
        the chapter in which the word/phrase was found."""
        nt_dict = pickle.load(open("nt_dict", "rb"))
        total_count = 0

        for key in nt_dict.keys():
            for i in nt_dict[key]:
                if self.phrase in nt_dict[key][i]:
                    print(key, i)
                    total_count += nt_dict[key][i].count(self.phrase)

        print("\nThis phrase occurs", total_count,
              "times in the New Testament.\n")


    def book_parse(self):
        """This method iterates through New Testament text to find
        user-entered word, submitted on the command line.
        This version only finds the number of user-words per
        chapter, sites the chapter where the word occurs most
        frequently, and calculates the total occurence of this
        word in the book as a whole."""

        with open("New Testament/" + self.text + ".txt") as book:
            total_word_count = 0
            chp_count = 0
            max_chp = 0
            words_in_chapter = []
            for chapter in book:
                chp_count += 1
                word_count = 0
                if self.key_word in chapter:
                    word_count += chapter.count(self.key_word)
                words_in_chapter.append(word_count)
                print("Occurence of \"{}\" in Chapter {}: ".format
                      (self.key_word, chp_count), word_count)
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
            print("\nTotal times that the word \"{}\" occurs in {}: "
                  .format(self.key_word, self.text), total_word_count,
                  "\nChapter where \"{}\" occurs most frequently: ".format
                  (self.key_word), max_chp)


    def most_common(self):
        """This method prints out tuples of the most common words
        found in the user-entered book. The first value in the tuple
        is the frequency of the word, followed by the word itself.
        Only words occurring X or more times are printed. Words occurring
        only once are added to hapaxes list."""

        with open("New Testament/" + self.text + ".txt") as book:
            chapters = [chp.split() for chp in book]

        idx = int(input("What chapter are you interested in?\n"))  # Chapter index
        count, words, chapter_list, chapter_tups, hapaxes = [], [], [], [], []
        chapter_count = 0

        for chapter in chapters:
            chapter_count += 1
            chapter_list.append(chapter_count)
            # List comprehension strips words of punctuation/case
            # and nests them in "words" list, organized by chapter:
            words.append([word.strip("();:\"\'?!,.-").lower()
                          for word in chapter])

        for chapter in words:
            # Creates a list of nested lists containing word lengths;
            # corresponds to nested "words" lists:
            count.append([chapter.count(word) for word in chapter])

        for i, _ in enumerate(chapter_list):
            chapter_tups.append(sorted(
                # Set comprehension producing (int, str) tuples from count/words lists:
                {(count, word) for count, word in zip(count[i], words[i])},
                reverse=True))  # Sorts the final list of sets in descending order by count.

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

        del_idx = chapter_tups[idx].index("for deletion")
        del chapter_tups[idx][del_idx:]

        for i, _ in enumerate(hapaxes):
            while hapaxes[i] in unwanted or hapaxes[i] in numbers:
                del hapaxes[i]
                hapaxes.append("for deletion")

        del_hap = hapaxes.index("for deletion")
        del hapaxes[del_hap:]

        print("\nMost commonly occurring words in the book of {}, Chapter {}:\n\n"
              .format(self.text, idx), chapter_tups[idx])

        haps = input(
            "\nWould you also like to return a list of words occurring only once? (Y or N):\n")
        if haps == "Y" or haps == 'y':
            print("\nWords that occur only once:\n", hapaxes[::-1])
