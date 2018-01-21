from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, ListProperty, StringProperty, DictProperty
from kivy.uix.listview import ListItemButton
import pickle

# from NT_Class import NewTestamentParse
# class_instance = NewTestamentParse()

search_input = ObjectProperty()


class AppStructure(BoxLayout):
    def search_book(self):
        # this code accepts text input in the search_input box and makes it a list; key: ListView class in kv file
        word = [self.search_input.text]
        self.search_results.item_strings = word


class TextButton(ListItemButton):
    pass


class AppRoot(BoxLayout):
    current_book = ObjectProperty()  # current_weather in kivy instruction book

    def show_text(self, book=None):
        self.clear_widgets()

        if self.current_book is None:
            self.current_book = CurrentBook()
        if book is not None:
            self.current_book.book = book

        self.current_book.search_nt_dict()
        self.add_widget(self.current_book)

    def show_app_structure(self):
        self.clear_widgets()
        self.add_widget(AppStructure())


class CurrentBook(BoxLayout):
    book = ListProperty()
    chapter = StringProperty()

    def search_nt_dict(self):
        nt_dict = pickle.load(open("nt_dict", "rb"))
        self.book = nt_dict["John"]
        self.chapter = str(nt_dict["John"][1])


class NewTestamentParseApp(App):
    def build(self):
        pass


if __name__ == '__main__':
    NewTestamentParseApp().run()

________________________________________________________________________________________________________________________
NOW ENTERING KV FILE INPUT:

    #: import main main
    #: import ListAdapter kivy.adapters.listadapter.ListAdapter

AppRoot:

<AppRoot> :
    AppStructure


<AppStructure> :
    orientation: 'vertical'
    search_input: search_box
    search_results: search_results_list
    BoxLayout:
        height: '40dp'
        size_hint_y: None
        TextInput:
            id: search_box
            size_hint_x: 50
            focus: True
            multiline: False
            on_text_validate: root.search_book()
        Button:
            text: 'Search'
            size_hint_x: 25
            on_press: root.search_book()
        Button:
            text: 'Book Parse'
            size_hint_x: 25
        Button:
            text: 'Phrase Parse'
            size_hint_x: 25
    ListView:
        id: search_results_list
        adapter:
            ListAdapter(data=[], cls=main.TextButton)
        item_strings: []
    Button:
        height: "40dp"
        size_hint_y: None
        text: "Cancel"
        on_press: app.root.show_text(None)


<TextButton> :
    on_press: app.root.show_text(self.text)


<CurrentBook> :
    orientation: "vertical"
    BoxLayout:
        Label:
            text: "{}".format(root.book)
            font_size: "30dp"
    Label:
        text: "{}".format(root.chapter)
        font_size: "30dp"
    BoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: "40dp"
        Button:
            text: "Search Book"
            on_press: app.root.show_app_structure()
        Button:
            text: "Parse"
