"""This module prints out tuples of the most common words
found in the user-entered book. The first value in the tuple
is the frequency of the word, followed by the word itself.
Only words occurring X or more times are printed."""


def most_common(text):
    """This is the sole function of this module."""
    with open("New Testament/" + text + ".txt") as book:
        chapters = [chp.split() for chp in book]

    count, words, chapter_list, chapter_tups = [], [], [], []
    chapter_count = 0

    for chapter in chapters:
        chapter_count += 1
        chapter_list.append(chapter_count)
        # List comprehension strips words of punctuation/case
        # and nests them in "words" list, organized by chapter:
        words.append([word.strip("();:\"\'?!,.-").lower() for word in chapter])

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

    # chapter_tups can be indexed three times: the first index indicates chapter,
    # the second indicates "most common words" tuples (sorted by highest count first), and
    # the last is indexed as 0 or 1, returning the count or the word (respectively).


if __name__ == "__main__":
    text = input("Which book would you like to parse?\n")
    if not text.istitle():
        text = text.title()
    most_common(text)
