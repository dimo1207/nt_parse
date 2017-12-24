from nt_most_cmn import nt_most_cmn

chapter_tups = nt_most_cmn("John")


final_range = 0
pronouns = ['he', 'her', 'him', 'she', 'they', 'them', 'you']
articles = ['the', 'a', 'an']
for i in range(len(chapter_tups)):
    for l in range(len(chapter_tups[i])):  # - final_range):
        if chapter_tups[i][l][1] in articles:
            final_range += 1
        if chapter_tups[i][l][1] in pronouns:
            final_range += 1
print(final_range)

print(len(chapter_tups[0]))

for i in range(len(chapter_tups)):
    for l in range(len(chapter_tups[i]) - final_range):
        if chapter_tups[i][l][1] in articles:
            del chapter_tups[i][l]
        if chapter_tups[i][l][1] in pronouns:
            del chapter_tups[i][l]
print(len(chapter_tups[0]))
