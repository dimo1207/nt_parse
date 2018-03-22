import os
import pickle
os.chdir('C:\\Users\\m_dim\\Documents\\Anaconda3\\NT Parse Scripts\\New Testament')
book_titles = [book.strip('.txt') for book in os.listdir()] # List of book titles
chapters_per_book, files, books, partitioned_books, nt_dict = [], [], [], [], {}

# Stores file contents, including the number of chapters per book;
# stored in 'chapters_per_book' and 'files' lists:
for book_file in os.listdir():
    with open(book_file, 'r') as b:
        text = b.readlines()
        chapters_per_book.append(len(text))
        files.append(text)

# Splits the chapters in each book,
# storing them as 260 separate strings in the 'books' list:
for book in files:
    for chapters in book:
        chapters.split('\n')
        books.append(chapters)

# Separates the chapters in each book into lists,
# appending them to the 'partitioned_books' list:
for chapters in chapters_per_book:
    partitioned_books.append(books[:chapters])
    books = books[chapters:]

# Stores nested keys in the 'nt_dict' dictionary:
# nt_dict[*book_keys][*chapters_per_book] = [*]
# (empty lists will later be overwritten by 'text')
for book, chapters in zip(book_titles, chapters_per_book):
    nt_dict[book] = {i: [] for i in range(1, chapters + 1)}

# Enters into nt_dict[book][chapter] (while simultaneously entering into
# the content that will be set to each [book][chapter] key pairing) and
# replaces the empty lists in 'nt_dict' with this content:
for book, content in zip(nt_dict, partitioned_books):
    for chapter, text in zip(nt_dict[book], content):
        nt_dict[book][chapter] = text


# pickle.dump(nt_dict, open('nt_dict', 'wb'))
# nt_dict = pickle.load(open('nt_dict', 'rb'))
