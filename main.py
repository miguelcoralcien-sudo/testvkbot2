# main.py — точка входа

import utils

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
            utils.add_note(text)
        elif choice == "2":
            utils.show_notes()
        elif choice == "3":
            utils.show_notes()
            try:
                index = int(input("Введите номер для удаления: "))
                utils.delete_note(index)
            except ValueError:
                print("Ошибка: введите число.")
        elif choice == "4":
            print("До свидания!")
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()