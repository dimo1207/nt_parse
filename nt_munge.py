from nt_most_cmn import nt_most_cmn

chapter_tups = nt_most_cmn("Revelation")

def munge():
    hapaxes = []
    x = -1  # Chapter index
    # Mask of unwanted words:
    unwanted = ['is', 'to', 'of', 'and', 'in', 'with', 'are', 'this',
                'the', 'a', 'an', 'he', 'her', 'him', 'she', 'they', 'them', 'you',
                'we', 'i', 'have', 'his', 'who', 'were', 'whose', 'when', 'was',
                'said', 'from', 'whom', 'but', 'what', 'that', 'it', 'then', 'which',
                'where', 'here', 'me', 'those', 'by', 'even', 'so', 'about', 'though',
                'as', 'also']

    for l in range(len(chapter_tups[x])):
        while chapter_tups[x][l][1] in unwanted:
            del chapter_tups[x][l]
            chapter_tups[x].append("for deletion")
        while chapter_tups[x][l][0] == 1:
            hapaxes.append(chapter_tups[x][l])
            del chapter_tups[x][l]
            chapter_tups[x].append("for deletion")

    del_idx = chapter_tups[x].index("for deletion")
    print(chapter_tups[x][:del_idx])
    # print(hapaxes)

munge()
