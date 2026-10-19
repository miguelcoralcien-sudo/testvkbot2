# utils.py — логика работы с заметками

import database

def add_note(text):
    notes = database.load_notes()
    notes.append(text)
    database.save_notes(notes)
    print(f"Заметка добавлена: {text}")

def show_notes():
    notes = database.load_notes()
    if not notes:
        print("Заметок нет.")
        return
    print("\n=== Ваши заметки ===")
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note}")

def delete_note(index):
    notes = database.load_notes()
    if 0 < index <= len(notes):
        removed = notes.pop(index - 1)
        database.save_notes(notes)
        print(f"Удалена заметка: {removed}")
    else:
        print("Ошибка: неверный номер.")