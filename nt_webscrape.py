#%%
import re
import pickle
import requests

"""Creates and imports the nt_dict object used in the nt_parse programs.
   This involves two functions: "retrieve_titles_and_texts()" and "import_nt_dict()". 
   The first is piped into the second to create a highly accessible dictionary object 
   of the full NRSV New Testament. The data is gathered entirely online, so no local files
   are required."""

def retrieve_titles_and_text():
    NT_Books = {
          'Matthew': 40, 'Mark': 41, 'Luke': 42, 'John': 43, 'Acts': 44, 'Romans': 45, 
          '1 Corinthians': 46, '2 Corinthians': 47, 'Galatians': 48, 'Ephesians': 49, 
          'Philippians': 50, 'Colossians': 51, '1 Thessalonians': 52, '2 Thessalonians': 53, 
          '1 Timothy': 54, '2 Timothy': 55, 'Titus': 56, 'Philemon': 57, 'Hebrews': 58, 
          'James': 59, '1 Peter': 60, '2 Peter': 61, '1 John': 62, '2 John': 63, 
          '3 John': 64, 'Jude': 65, 'Revelation': 66
          }
    nt_titles = [title for title in NT_Books.keys()]
    nt_content = []

    for book in NT_Books.keys(): # Sets the URL for each book in the above dictionary
        if book[0].isdigit(): # (book titles with numbers have a separate url format)
                URL = 'http://www.devotions.net/bible/{}-{}{}.htm'.format(
                    NT_Books[book], book[0], book[2:].lower())
        else:
            URL = 'http://www.devotions.net/bible/{}{}.htm'.format(
                NT_Books[book], book.lower())

        # Retrieves the content and stores it as a string
        r = requests.get(URL)
        content = str(r.text)

        # Indexes the start of the content, and uses this index to slice out unwanted text
        # Finally, splits the content at each chapter heading (designated by <p>)
        form = '(' + book
        idx = content.index(form)
        content = content[idx:]
        content = content.split('<p>')

        # Allows the subscript to be indexed by searching within each line of the text
        # (indexing the subscript directly fails):
        for line in content:
            if '<center><script' in line:
                idx2 = content.index(line)
                break
        content = content[:idx2] # Slices out unwanted text

        # Excises newlines and appends the altered content to a fresh final_content list
        final_content = []
        for chapter in content:
            final_content.append(chapter.replace('\n', ' '))

        # Stores the end product of the loop
        nt_content.append(final_content)

    # Returns the final product of importing and processing each title in NT_Books dictionary
    return nt_titles, nt_content


def import_nt_dict(pickled=False):
    book_titles, nt_content = retrieve_titles_and_text()
    chapters_per_book = [len(book) for book in nt_content]
    books, partitioned_books, nt_dict = [], [], {}

    # Splits the chapters in each book,
    # storing them as 260 separate strings in the 'books' list:
    for book in nt_content:
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
    	nt_dict[book] = {i: [] for i in range(1, chapters+1)}

    # Enters into nt_dict[book][chapter] (while simultaneously entering into
    # the content that will be set to each [book][chapter] key pairing) and
    # replaces the empty lists in 'nt_dict' with this content:
    for book, content in zip(nt_dict, partitioned_books):
        for chapter, text in zip(nt_dict[book], content):
            nt_dict[book][chapter] = text


    if pickled==True: # Pickles completed nt_dict object
        pickle.dump(nt_dict, open('nt_dict.pickle', 'wb'))

    return nt_dict


if __name__ == '__main__':
    nt_dict = import_nt_dict(pickled=False)
    print(nt_dict['Luke'][3])