from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from notes import Note, NoteManager

class ScreenButton(Button):
    def __init__(self, screen, direction="right", goal="main", note_name="new note", note_text="new note text", **kw):
        super().__init__(**kw)
        self.screen = screen
        self.direction = direction
        self.goal = goal
        self.note_name = note_name
        self.note_text = note_text

    def on_press(self):
        self.screen.manager.transition.direction = self.direction
        if self.goal == 'note':
            self.screen.manager.get_screen('note').note = Note(self.note_name, self.note_text)
        self.screen.manager.current = self.goal


class MainScreen(Screen):

    notes_list_layout = BoxLayout(orientation="vertical", pos_hint={"top":1})

    def __init__(self, **kw):
        super().__init__(**kw)

        new_note_btn = ScreenButton(self, 
                                    text="new note",
                                    size_hint=(0.10, 0.10), pos_hint={'top':0.15, "right":0.95},
                                    goal="note", direction="up")

       
        self.add_widget(new_note_btn)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.update_notes_list()

    def update_notes_list(self):
        self.remove_widget(self.notes_list_layout)
        self.notes_list_layout = BoxLayout(orientation="vertical", pos_hint={"top":1})
        self.notes_list = NoteManager().get_notes_list()

        notes_num = len(self.notes_list)
        for note in self.notes_list:
            note_wrapper = BoxLayout(size_hint=(0.75, notes_num/100), size_hint_max_y=100)
            note_name = Label(text=note.get_name())
            edit_note_btn = ScreenButton(self, 
                                        text="edit",
                                        size_hint=(0.25,0.25),
                                        goal="note", direction="down", 
                                        note_name=note.get_name(), note_text=note.get_text()) 
            note_wrapper.add_widget(note_name)
            note_wrapper.add_widget(edit_note_btn)
            self.notes_list_layout.add_widget(note_wrapper)
        self.add_widget(self.notes_list_layout)


class NoteScreen(Screen):
    note = None
    header = TextInput(size_hint=(1, .15))
    text_field = TextInput()

    def __init__(self, **kw):
        super().__init__(**kw)
       
        layout_wrapper = BoxLayout(orientation="vertical")
        bck_btn = ScreenButton(self, text="<--", size_hint=(.1,.1), size_hint_min=(50,50))
        layout = BoxLayout(orientation="vertical", size_hint=(.75, 1), pos_hint={'center_x':0.5})

        layout.add_widget(self.header)
        layout.add_widget(self.text_field)

        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, .1))

        button_save = Button(text='Save')
        button_save.on_press = self.create_note

        button_disscard = Button(text='delete note')
        button_disscard.on_press = self.delete_note

        buttons_layout.add_widget(button_save)
        buttons_layout.add_widget(button_disscard)

        layout_wrapper.add_widget(bck_btn)
        layout_wrapper.add_widget(layout)
        layout_wrapper.add_widget(buttons_layout)
        
        self.add_widget(layout_wrapper)
    
    def update_existing_note(self):
        if self.note:
            self.header.text = self.note.get_name()
            self.text_field.text = self.note.get_text()
        
    
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.update_existing_note()    

    def create_note(self):
        self.note.set_name(self.header.text)
        self.note.set_text(self.text_field.text)
        NoteManager().create_note(self.note)
        self.manager.current = 'main'

    def delete_note(self):
        NoteManager().delete_note(self.note)
        self.manager.current = 'main'


class NotesApp(App):
    def build(self):
        
        sm = ScreenManager()

        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(NoteScreen(name="note"))
        
        return sm

if __name__=="__main__":
    NotesApp().run()