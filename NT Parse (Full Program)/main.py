from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.listview import ListItemLabel
import pickle


class BookListButton(ListItemButton):
    """Imports object referenced in .kv file."""
    pass

class BookListLabel(ListItemLabel):
    """Imports object referenced in .kv file."""
    pass

class CurrentBook(BoxLayout):
    """Imports object referenced in .kv file."""
    pass

class NTParse(BoxLayout):
    """Primary class of the app; includes all major functions."""

    # Connects the value in the TextInput widget to these fields:
    book_name_text_input = ObjectProperty()
    word_phrase_text_input = ObjectProperty()
    chapter_text_input = ObjectProperty()


    # The following three functions handle text input and set it to different variables:
    def search_text(self):
        """Returns the text found in the TextInput box that follows "Book Name:".
        If no text is entered, "John" is returned as the default."""
        if self.book_name_text_input.text:
            text = (self.book_name_text_input.text).title()
            return text
        return "John"  # Default input

    def search_phrase(self):
        """Returns the text found in the TextInput box that follows "Word or Phrase:".
        If no text is entered, "love" is returned as the default."""
        if self.word_phrase_text_input.text:
            phrase = self.word_phrase_text_input.text
            return phrase
        return "love"  # Default input

    def search_chapter(self):
        """Returns the text found in the TextInput box that follows "Chapter:".
        If no text is entered, 1 is returned as the default."""
        if self.chapter_text_input.text:
            idx = self.chapter_text_input.text
            return idx
        return 1  # Default input


    def custom_context_manager(primary_function):
        """Decorator function. Provides standard enter/exit requirements for the primary functions."""
        def wrapper_function(self):
            self.nt_dict = pickle.load(
                open("nt_dict", "rb"))  # imports the raw data
            self.output_list.adapter.data = []  # clears the "data" list
            # executes the primary function that's being decorated
            primary_function(self)
            # resets listview with updated "data" list
            self.output_list._trigger_reset_populate()
            return
        return wrapper_function  # not closing parentheses makes the function "ready to execute"

    # Primary functions of the app (three in total):
    @custom_context_manager
    def parse(self):
        """This method iterates through New Testament text to find
        user-entered word, finds the number of user-words per
        chapter, sites the chapter where the word occurs most
        frequently, and calculates the total occurence of this
        word in the book as a whole."""
        text = self.search_text()
        key_word = self.search_phrase()
        
        # The following check keeps the app from crashing on bad input:
        if text not in self.nt_dict.keys():
            return self.reset_app()

        total_word_count, chp_count, max_chp = 0, 0, 0
        parsed_text, words_in_chapter = [], []
        for chapter in self.nt_dict[text]:
            chp_count += 1
            word_count = 0
            if key_word in self.nt_dict[text][chapter]:
                word_count += self.nt_dict[text][chapter].count(key_word)
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

        # "Extends" data list with desired output:
        self.output_list.adapter.data.extend([total_times])
        self.output_list.adapter.data.extend([most_freq_chap])
        self.output_list.adapter.data.extend([str(x) for x in parsed_text])


    @custom_context_manager
    def search(self):
        """This method searches each chapter of each book
        in nt_dict for the user-entered phrase or word.
        If found, the function returns the book title and
        the chapter in which the phrase/word was found."""
        phrase = self.search_phrase()
        total_count = 0
        searched_text = []

        for key in self.nt_dict.keys():
            for i in self.nt_dict[key]:
                if phrase in self.nt_dict[key][i]:
                    searched_text.append(key + " " + str(i))
                    total_count += self.nt_dict[key][i].count(phrase)

        search_result = "'{}' occurs ".format(phrase[0].upper() + phrase[1:]) + str(total_count) + " times in the New Testament:"

        # "Extends" data list with desired output:
        self.output_list.adapter.data.extend([str(search_result)])
        self.output_list.adapter.data.extend([str(x) for x in searched_text])


    @custom_context_manager
    def most_common(self):
        """This method prints out tuples of the most common words
        found in the user-entered book. The first value in the tuple
        is the frequency of the word, followed by the word itself.
        Only words occurring X or more times are printed."""
        text = self.search_text()
        idx = int(self.search_chapter()) - 1

        # The following checks keep the app from crashing on bad input:
        if text not in self.nt_dict.keys():
            text = "John"
        if idx not in self.nt_dict[text].keys():
            idx = 0

        count, words, chapter_list, chapter_tups, hapaxes = [], [], [], [], []
        chapter_count = 0

        for chapter in self.nt_dict[text]:
            chapter_count += 1
            chapter_list.append(chapter_count)
            # List comprehension strips words of punctuation/case
            # and nests them in "words" list, organized by chapter:
            words.append([word.strip("();:\"\'?!,.-").lower()
                          for word in self.nt_dict[text][chapter].split()])

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

        # The following del statements index "for deletion" in each list,
        # and then delete each value following that index via slicing:
        del chapter_tups[idx][chapter_tups[idx].index("for deletion"):]
        del hapaxes[hapaxes.index("for deletion"):]

        label_1 = "Most commonly occurring words in the book of {}, Chapter {}:".format(text, idx + 1)
        label_2 = "Words that occur only once:" 

        # "Extends" data list with desired output:
        self.output_list.adapter.data.extend([label_1])
        self.output_list.adapter.data.extend([str(x) for x in chapter_tups[idx]])
        self.output_list.adapter.data.extend([label_2])
        self.output_list.adapter.data.extend([str(x) for x in hapaxes[::-1]])


    def clear(self):
        """Clears ListView contents and resets display."""
        self.output_list.adapter.data = []
        self.output_list._trigger_reset_populate()

    def reset_app(self):
        """Resets the app to starting conditions."""
        self.clear_widgets()
        self.add_widget(NTParse())

    def store_button_text(self, button_text):
        """Stores all of the text displayed on the button being pressed."""
        self.button_text = button_text

    def show_text(self, button_text):
        """Launches CurrentBook widget after clearing any existing widgets."""
        # The following check keeps the app from crashing on bad input:
        if self.button_text[-1] in [")", ":", "]"]:
            return self.reset_app()
        elif "Total" in self.button_text:
            return self.reset_app()
        self.clear_widgets()
        self.current_book = CurrentBook()
        self.add_widget(self.current_book)

    def return_desired_book(self):
        """Parses the button_text stored on press.
        The processed data is then passed to the "CurrentBook" widget as a label."""
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
        """Parses the button_text stored on press.
        The processed data is then passed to the "CurrentBook" widget as a label."""
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
        """Uses the data from button_text as keys in nt_dict.
        Returns the Bible text specified by the processed button_text data."""
        nt_dict = pickle.load(open("nt_dict", "rb"))
        book = ""
        chapter = 1

        for key in nt_dict.keys():
            if key in self.button_text:
                book = key

        # covers cases with two-digit word count returns (book parse only):
        if self.button_text[-4] == ":":
            # covers cases with one-digit chapters:
            if self.button_text[-6] == " ":
                chapter = int(self.button_text[-5:-4])
            # covers cases with two-digit chapters:
            chapter = int(self.button_text[-6:-4])
        # covers one-digit word count returns (book parse only):
        elif "Occurence" in self.button_text:
            chapter = int(self.button_text[-5:-3])
        else:
            # covers full parse chapters only:
            chapter = int(self.button_text[-2:])

        outcome = nt_dict[book][chapter].split()
        # The following generator is used to yield "outcome" contents to ListView labels.
        # It limits the length of each label to 11 words to ensure the text is displayed properly:
        for start in range(0, len(outcome), 11):
            yield " ".join(outcome[start:start + 11])



class NTParseApp(App):
    def build(self):
        return NTParse()


NTParseApp().run()
