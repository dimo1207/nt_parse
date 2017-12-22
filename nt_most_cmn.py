"""This module prints out tuples of the most common words
found in the user-entered book. The first value in the tuple
is the frequency of the word, followed by the word itself.
Only words occurring 5 or more times are printed."""


print("Which book would you like to parse?")


def nt_most_cmn(inpuT):
    with open("New Testament/" + str(inpuT) + ".txt") as book:
        chapters = [chp.split() for chp in book]
        count = []
        words = []
        chapter_list = []
        chapter_count = 0
        chapter_tups = []

        for chapter in chapters:
            chapter_count += 1
            chapter_list.append(chapter_count)
            count.append([chapter.count(word) for word in chapter])
            words.append([word for word in chapter])

        # for ls in words:
        #     for word in ls:
        #     # if word.startswith("("):
        #     #     word = word[1:]
        #         elif word.endswith("\""):
        #             word.strip("\"")
        #         elif word.endswith("?"):
        #             word.strip("?")
        #         elif word.endswith(")"):
        #             word.strip(")")
        #         elif word.endswith("!"):
        #             word.strip("!")
        #         elif word.endswith(","):
        #             word.strip(",")
        #         elif word.endswith("."):
        #             word.strip(".")

        for i in range(len(chapter_list)):
            chapter_tups.append(sorted({(count, word) for count, word in zip(count[i], words[i])}, reverse=True))
            
        print(chapter_tups[0])
        # print((chapter_tups[0]))
        # for i in range(len(chapter_tups)):
        #     print([item[i] for item in chapter_tups])
        


if __name__ == "__main__":
    nt_most_cmn(input())
