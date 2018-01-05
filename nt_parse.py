"""This code iterates through New Testament text to find
user-entered word, submitted on the command line.
This version only finds the number of user-words per
chapter, sites the chapter where the word occurs most
frequently, and calculates the total occurence of this
word in the book as a whole."""


def nt_parse():
    """This is the sole function of the module."""
    text = input("Which book would you like to parse?\n")
    if text[0].islower():
        text = text.title()
    key_word = input("What word would you like to find?\n")

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
        print("\nTotal times that the word \"{}\" occurs in {}: "
              .format(key_word, text), total_word_count)
        print("\nChapter where \"{}\" occurs most frequently: ".format
              (key_word), max_chp)


if __name__ == "__main__":
    nt_parse()
