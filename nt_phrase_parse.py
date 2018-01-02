import re

def nt_phrase_parse(phrase):
    full = ""
    phrase = phrase.lower()
    with open("New Testament/" + text + ".txt", 'r') as book:
        for chapter in book:
            full += chapter.lower()

    for x in re.finditer(phrase, full):
        print("Phrase found:", x.start(), x.end())
        print(full[x.start()-50:x.start()+50])








if __name__ == "__main__":
    phrase = input("What phrase are you looking for?\n")
    nt_phrase_parse(phrase)
