# Скрипт для заметок — всё в одном файле

notes = []  # список для хранения заметок

def add_note(text):
    notes.append(text)
    print(f"Заметка добавлена: {text}")

def show_notes():
    if not notes:
        print("Заметок нет.")
        return
    print("\n=== Ваши заметки ===")
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note}")

def delete_note(index):
    if 0 < index <= len(notes):
        removed = notes.pop(index - 1)
        print(f"Удалена заметка: {removed}")
    else:
        print("Ошибка: неверный номер.")

def main():
    while True:
        print("\n=== Заметки ===")
        print("1. Добавить заметку")
        print("2. Показать все заметки")
        print("3. Удалить заметку")
        print("4. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            text = input("Введите текст заметки: ")
            add_note(text)
        elif choice == "2":
            show_notes()
        elif choice == "3":
            show_notes()
            try:
                index = int(input("Введите номер для удаления: "))
                delete_note(index)
            except ValueError:
                print("Ошибка: введите число.")
        elif choice == "4":
            print("До свидания!")
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()