from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager


class ScreenButton(Button):
    def __init__(self, screen, direction="right", goal="main", note_name ="", note_text="", **kw):
        '''
            To get context data for existing note pass:
            `note_name`
            `note_text`
        '''
        super().__init__(**kw)
        self.screen = screen
        self.direction = direction
        self.goal = goal
        self.context_data = {
            "name":note_name,
            "text":note_text
        }

    def on_press(self):
        self.screen.manager.transition.direction = self.direction
        self.screen.manager.current = self.goal


class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        notes_list = BoxLayout(orientation="vertical", pos_hint={"top":1})
        notes_num = 15
        for i in range(notes_num):
            note_wrapper = BoxLayout(size_hint=(0.75, notes_num/100), size_hint_max_y=100)
            note_name = Label(text="test_note")
            edit_note_btn = ScreenButton(self, 
                                        text="edit", 
                                        size_hint=(0.25,0.25),
                                        goal="note", direction="down",
                                        note_name="Edited", note_text="text of th note to be edited")
            note_wrapper.add_widget(note_name)
            note_wrapper.add_widget(edit_note_btn)
            notes_list.add_widget(note_wrapper)

        new_note_btn = ScreenButton(self, 
                                    text="new note",
                                    size_hint=(0.10, 0.10), pos_hint={'top':0.15, "right":0.95},
                                    goal="note", direction="up")

        self.add_widget(notes_list)
        self.add_widget(new_note_btn)



class NoteScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        layout_wrapper = BoxLayout(orientation="vertical")
        bck_btn = ScreenButton(self, text="<--", size_hint=(.1,.1), size_hint_min=(50,50))
        layout = BoxLayout(orientation="vertical", size_hint=(.75, 1), pos_hint={'center_x':0.5})

        header = Label(text="Here will be note name", size_hint=(1, .15))
        text_field = TextInput(text="Placeholder text for new note")
        
        layout.add_widget(header)
        layout.add_widget(text_field)

        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, .1))
        button_save = Button(text='Save')
        button_disscard = Button(text='delete note')
        buttons_layout.add_widget(button_save)
        buttons_layout.add_widget(button_disscard)

        
        layout_wrapper.add_widget(bck_btn)
        layout_wrapper.add_widget(layout)
        layout_wrapper.add_widget(buttons_layout)
        
        self.add_widget(layout_wrapper)

class NotesApp(App):
    def build(self):
        sm = ScreenManager()
        
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(NoteScreen(name="note"))

        return sm

if __name__=="__main__":
    NotesApp().run()