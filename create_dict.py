import os
import pickle
os.chdir('C:\\Users\\m_dim\\Documents\\Anaconda3\\NT Parse Scripts\\New Testament')
book_keys = [book.strip('.txt') for book in os.listdir()]
chp_list, chps, final, txt_list, nt_dict = [], [], [], [], {}

for book in os.listdir():
    with open(book, 'r') as b:
        f = b.readlines()
        chp_list.append(len(f))
        chps.append(f)

for chp in chps:
    for txt in chp:
        txt.split('\n')
        final.append(txt)

for length in chp_list:
    txt_list.append(final[:length])
    final = final[length:]

for book, chp in zip(book_keys, chp_list):
    nt_dict[book] = {i: [] for i in range(1, chp + 1)}

for i, book in zip(nt_dict, txt_list):
    for chp, ls in zip(nt_dict[i], book):
        nt_dict[i][chp] = ls


# pickle.dump(nt_dict, open('nt_dict.pickle', 'wb'))
# nt_dict = pickle.load(open('nt_dict.pickle', 'rb'))
