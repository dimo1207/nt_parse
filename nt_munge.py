from nt_most_cmn import nt_most_cmn

chapter_tups = nt_most_cmn("John")

def munge():
    # Mask of unwanted words:
    unwanted = ['is', 'to', 'of', 'and', 'in', 'with', 'are', 'this',
                'the', 'a', 'an', 'he', 'her', 'him', 'she', 'they', 'them', 'you',
                'we', 'i', 'have', 'his', 'who', 'were', 'whose', 'when', 'was',
                'said', 'from', 'whom', 'but', 'what', 'that', 'it', 'then', 'which',
                'where', 'here']

    for l in range(len(chapter_tups[0])):
        while chapter_tups[0][l][1] in unwanted:
            del chapter_tups[0][l]
            chapter_tups[0].append("for deletion")
        while chapter_tups[0][l][0] == 1:
            del chapter_tups[0][l]
            chapter_tups[0].append("for deletion")

    del_idx = chapter_tups[0].index("for deletion")
    return (chapter_tups[0][:del_idx])
munge()
