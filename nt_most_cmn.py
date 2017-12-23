"""This module prints out tuples of the most common words
found in the user-entered book. The first value in the tuple
is the frequency of the word, followed by the word itself.
Only words occurring 5 or more times are printed."""


print("Which book would you like to parse?")


def nt_most_cmn(inpuT):
    with open("New Testament/" + str(inpuT) + ".txt") as book:
        chapters = [chp.split() for chp in book]

    count, words, chapter_list, chapter_tups = [], [], [], []
    chapter_count = 0

    for chapter in chapters:
        chapter_count += 1
        chapter_list.append(chapter_count)
        # List comprehension strips words of punctuation/case and nests them in "words" list, organized by chapter:
        words.append([word.strip("();:\"\'?!,.").lower() for word in chapter]) 

    for chapter in words:
        # Creates a list of nested lists containing word lengths; corresponds to nested "words" lists:
        count.append([chapter.count(word) for word in chapter])

    for i in range(len(chapter_list)):
        chapter_tups.append(sorted({(count, word) for count, word in zip(count[i], words[i])}, reverse=True))

    # Test:
    for i in range(len(chapter_tups)):
        for l in range(len(chapter_tups[i])):
            print(chapter_tups[i][l][1]) 
    # chapter_tups can be indexed three times: the first indicates chapter, 
    # the second indicates most common words tups (sorted by highest count first), and 
    # the last is indexed as 0 or 1, returing the count or the word (respectively).

if __name__ == "__main__":
    nt_most_cmn(input())
