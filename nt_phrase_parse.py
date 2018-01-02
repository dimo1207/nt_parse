import pickle
nt_dict = pickle.load(open("nt_dict", "rb"))


def nt_phrase_parse(phrase):
    for key in nt_dict.keys():
        for i in nt_dict[key]:
            if phrase in nt_dict[key][i]:
                print(key, i)


if __name__ == "__main__":
    phrase = input("What phrase are you looking for?\n")
    nt_phrase_parse(phrase)
