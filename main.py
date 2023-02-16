from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager

class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        notes_list = BoxLayout(orientation="vertical", pos_hint={"top":1})
        notes_num = 15
        for i in range(notes_num):
            note_wrapper = BoxLayout(size_hint=(0.75, notes_num/100), size_hint_max_y=100)
            note_name = Label(text="test_note")
            edit_note_btn = Button(text="edit", size_hint=(0.25,0.25))
            note_wrapper.add_widget(note_name)
            note_wrapper.add_widget(edit_note_btn)
            notes_list.add_widget(note_wrapper)

        new_note_btn = Button(text="new note",size_hint=(0.10, 0.10), pos_hint={'top':0.15, "right":0.95})

        self.add_widget(notes_list)
        self.add_widget(new_note_btn)



class NoteScreen(Screen):
    ...

class NotesApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(NoteScreen(name="note"))
        return sm

if __name__=="__main__":
    NotesApp().run()