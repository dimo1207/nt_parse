def nt_parse():

    print("Which book would you like to parse?")
    text = input()
    print("What word would you like to find?")
    key_word = input()

    with open("Bible/" + text + ".txt") as book:
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
        for x in words_in_chapter:
            if total_word_count == 0:
                max_chp = "n/a"
            elif words_in_chapter.count(most_freq) > 1:
                 max_chp = []
                 for y, z in enumerate(words_in_chapter):
                     if z == most_freq:
                        max_chp.append(y + 1)
            elif x == max(words_in_chapter):
                max_chp = (words_in_chapter.index(x) + 1)
        print("\nTotal times that the word \"{}\" occurs in {}: "
             .format(key_word, text), total_word_count)
        print("\nChapter where \"{}\" occurs most frequently: ".format
             (key_word), max_chp)

nt_parse()
