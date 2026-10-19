# database.py — работа с данными

import json

NOTES_FILE = "notes.json"

def load_notes():
    """Загружает заметки из файла."""
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_notes(notes):
    """Сохраняет заметки в файл."""
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)
