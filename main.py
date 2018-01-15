from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
import pickle


class BookListButton(ListItemButton):
    pass

class CurrentBook(BoxLayout):
    pass

class NTParse(BoxLayout):

    # Connects the value in the TextInput widget to these
    # fields
    book_name_text_input = ObjectProperty()
    word_phrase_text_input = ObjectProperty()
    chapter_text_input = ObjectProperty()
    output_list = ObjectProperty()
    current_book = ObjectProperty()

    def search_text(self):
        if self.book_name_text_input.text:
            text = self.book_name_text_input.text
            return text
        return "John"

    def search_phrase(self):
        if self.word_phrase_text_input.text:
            phrase = self.word_phrase_text_input.text
            return phrase
        return "love"

    def search_chapter(self):
        if self.chapter_text_input.text:
            idx = self.chapter_text_input.text
            return idx
        return 1

    def parse(self):
        self.output_list.adapter.data = []
        nt_dict = pickle.load(open("nt_dict", "rb"))
        text = self.search_text()
        key_word = self.search_phrase()

        total_word_count, chp_count, max_chp = 0, 0, 0
        parsed_text, words_in_chapter = [], []
        for chapter in nt_dict[text]:
            chp_count += 1
            word_count = 0
            if key_word in nt_dict[text][chapter]:
                word_count += nt_dict[text][chapter].count(key_word)
            words_in_chapter.append(word_count)
            parsed_text.append("Occurence of \"{}\" in {}, Chapter {}: ".format
                (key_word, text, chp_count) + str(word_count))
            total_word_count += word_count
            most_freq = max(words_in_chapter)
        for cnt in words_in_chapter:
            if total_word_count == 0:
                max_chp = "n/a"
            elif words_in_chapter.count(most_freq) > 1:
                max_chp = []
                for i, word in enumerate(words_in_chapter):
                    if word == most_freq:
                        max_chp.append(i + 1)
            elif cnt == max(words_in_chapter):
                max_chp = (words_in_chapter.index(cnt) + 1)
        total_times = "Total times that the word \"{}\" occurs in {}: ".format(key_word, text) + str(total_word_count)
        most_freq_chap = "Chapter where \"{}\" occurs most frequently: ".format(key_word) + str(max_chp)

        # Add the output to the ListView
        self.output_list.adapter.data.extend([total_times])
        self.output_list.adapter.data.extend([most_freq_chap])
        self.output_list.adapter.data.extend([str(x) for x in parsed_text])

        # Reset the ListView
        self.output_list._trigger_reset_populate()


    def search(self):
        self.output_list.adapter.data = []
        nt_dict = pickle.load(open("nt_dict", "rb"))
        phrase = self.search_phrase()
        total_count = 0
        searched_text = []

        for key in nt_dict.keys():
            for i in nt_dict[key]:
                if phrase in nt_dict[key][i]:
                    searched_text.append(key + " " + str(i))
                    total_count += nt_dict[key][i].count(phrase)

        search_result = "'{}' occurs ".format(phrase[0].upper() + phrase[1:]) + str(total_count) + " times in the New Testament:"

        # Add the output to the ListView
        self.output_list.adapter.data.extend([str(search_result)])
        self.output_list.adapter.data.extend([str(x) for x in searched_text])

        # Reset the ListView
        self.output_list._trigger_reset_populate()


    def most_common(self):
        self.output_list.adapter.data = []
        nt_dict = pickle.load(open("nt_dict", "rb"))
        text = self.search_text()
        # Chapter index (-1 to adjust for indexing rules):
        idx = int(self.search_chapter()) - 1

        # This code raises an error if the chapter entered is not in the book:
        # if idx > len(nt_dict[self.text]) or idx <= -1:
        #     raise IndexError(
        #         "The book of {} has {} chapters. Please enter a number between {} and {}."
        #         .format(self.text, len(nt_dict[self.text]), 1, len(nt_dict[self.text])))
        count, words, chapter_list, chapter_tups, hapaxes = [], [], [], [], []
        chapter_count = 0

        for chapter in nt_dict[text]:
            chapter_count += 1
            chapter_list.append(chapter_count)
            # List comprehension strips words of punctuation/case
            # and nests them in "words" list, organized by chapter:
            words.append([word.strip("();:\"\'?!,.-").lower()
                          for word in nt_dict[text][chapter].split()])

        for chapter in words:
            # Creates a list of nested lists containing word lengths;
            # corresponds to nested "words" lists:
            count.append([chapter.count(word) for word in chapter])

        for i, _ in enumerate(chapter_list):
            chapter_tups.append(sorted(
                # Set comprehension producing (int, str) tuples from count/words lists:
                {(count, word) for count, word in zip(count[i], words[i])},
                reverse=True))  # Sorts the final list of sets in descending order by count.

        # Masks of unwanted words:
        numbers = [str(x) for x in range(75)]
        unwanted = ['is', 'to', 'of', 'and', 'in', 'with', 'are', 'this', 'for',
                    'the', 'a', 'an', 'he', 'her', 'him', 'she', 'they', 'them', 'you',
                    'we', 'i', 'have', 'his', 'who', 'were', 'whose', 'when', 'was',
                    'said', 'from', 'whom', 'but', 'what', 'that', 'it', 'then', 'which',
                    'where', 'here', 'me', 'those', 'by', 'even', 'so', 'about', 'though',
                    'as', 'also']

        for i, _ in enumerate(chapter_tups[idx]):
            while chapter_tups[idx][i][1] in unwanted or chapter_tups[idx][i][1] in numbers:
                del chapter_tups[idx][i]
                chapter_tups[idx].append("for deletion")
            while chapter_tups[idx][i][0] == 1:
                hapaxes.append(chapter_tups[idx][i][1])
                del chapter_tups[idx][i]
                chapter_tups[idx].append("for deletion")

        for i, _ in enumerate(hapaxes):
            while hapaxes[i] in unwanted or hapaxes[i] in numbers:
                del hapaxes[i]
                hapaxes.append("for deletion")
        # the following del statements index "for deletion" in each list,
        # and then delete each value following that index via slicing:
        del chapter_tups[idx][chapter_tups[idx].index("for deletion"):]
        del hapaxes[hapaxes.index("for deletion"):]

        label_1 = "Most commonly occurring words in the book of {}, Chapter {}:".format(text, idx + 1)
        label_2 = "Words that occur only once:" 

        # Add the output to the ListView
        self.output_list.adapter.data.extend([label_1])
        self.output_list.adapter.data.extend([str(x) for x in chapter_tups[idx]])
        self.output_list.adapter.data.extend([label_2])
        self.output_list.adapter.data.extend([str(x) for x in hapaxes[::-1]])

        # Reset the ListView
        self.output_list._trigger_reset_populate()


    def clear(self):

        self.output_list.adapter.data = []

        self.output_list._trigger_reset_populate()

    def reset_app(self):

        self.clear_widgets()

        self.add_widget(NTParse())

    def show_text(self, button_text):

        self.clear_widgets()
        self.current_book = CurrentBook()

        
        # self.output_list.adapter.data.extend(["test"])
        # self.output_list._trigger_reset_populate()

        self.add_widget(self.current_book)
    
    def store_button_text(self, button_text):

        self.button_text = button_text

    def return_desired_book(self):
        nt_dict = pickle.load(open("nt_dict", "rb"))
        for key in nt_dict.keys():
            if key in self.button_text:  # checks for key inclusion
                # Everything that follows checks for books that begin with numbers:
                key_index = self.button_text.index(key)
                if key_index is 0:
                    return key
                elif self.button_text[key_index - 2] == "1":
                    if key[0] == "2":
                        key.replace(key[0], "1")
                        return key
                    elif key[0] == "3":
                        key.replace(key[0], "1")
                        return key
                    key = "1 " + key
                    return key
                elif self.button_text[key_index - 2] == "2":
                    if key[0] == "1":
                        key.replace(key[0], "2")
                        return key
                    elif key[0] == "3":
                        key.replace(key[0], "2")
                        return key
                    key = "2 " + key
                    return key
                elif self.button_text[key_index - 2] == "3":
                    if key[0] == "1":
                        key.replace(key[0], "3")
                        return key
                    elif key[0] == "1":
                        key.replace(key[0], "3")
                        return key
                    key = "3 " + key
                    return key
                return key

    def return_desired_chapter(self):
        # covers cases with two-digit word count returns (book parse only):
        if self.button_text[-4] == ":":
            # covers cases with one-digit chapters:
            if self.button_text[-6] == " ":
                chapter = str(self.button_text[-5:-4])
            # covers cases with two-digit chapters:
            chapter = str(self.button_text[-6:-4])
        # covers one-digit word count returns (book parse only):
        elif "Occurence" in self.button_text:
            chapter = str(self.button_text[-5:-3])
        else:
            # covers full parse chapters only:
            chapter = str(self.button_text[-2:])
        return chapter

    def return_bible_text(self):
        nt_dict = pickle.load(open("nt_dict", "rb"))
        book = ""
        chapter = ""

        for key in nt_dict.keys():
            if key in self.button_text:
                book = key

        if len(self.button_text) == 43:
            chapter = int(self.button_text[-6:-4])
        elif "Occurence" in self.button_text:
            chapter = int(self.button_text[-5:-3])
        else:
            chapter = int(self.button_text[-2:])

        outcome = nt_dict[book][chapter].split()

        for start in range(0, len(outcome), 12):

            yield " ".join(outcome[start:start + 12])



class NTParseApp(App):
    def build(self):
        return NTParse()


NTParseApp().run()
