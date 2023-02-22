from pathlib import Path

NOTES_DIR = 'notes'


class Note():
    def __init__(self, name:str=None, text:str=None):
        self.name = name
        self.text = text
    
    def set_name(self, name):
        self.name = name
    def get_name(self):
        return self.name

    def set_text(self, text):
        self.text = text
    def get_text(self):
        return self.text


def _create_notes_dir(notes_dir):
    path = Path(Path().cwd(), notes_dir)
    if not path.is_dir():
        path.mkdir(parents=True)
    return path
        
class NoteManager():
    def __init__(self):
        path = Path(Path().cwd(), NOTES_DIR)
        if not path.is_dir():
            path.mkdir(parents=True)
        self.notes_dir = path


    def create_note(self, note: Note):
        dir_path = Path(Path().cwd(), self.notes_dir)
        full_path = Path(dir_path, note.get_name()+'.txt')
        if not full_path.is_file():
            _create_notes_dir(self.notes_dir)
        with full_path.open('w') as new_note:
            new_note.write(note.get_text())

    def delete_note(self, note: Note):
        Path(self.notes_dir, note.get_name()+'.txt').unlink(missing_ok=True)

    def delete_note_by_filename(self, filename: str):
        Path(self.notes_dir, filename).unlink(missing_ok=True)

    def get_notes_list(self):
        dir_path  = Path(Path().cwd(), self.notes_dir)
        notes_list = []
        for filename in dir_path.iterdir():
            with open(Path(dir_path, filename), 'r') as note_file:
                notes_list.append(Note(
                    filename.stem, note_file.read()
                ))

        return notes_list

