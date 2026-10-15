# Калькулятор скидок для магазина кофе

# Каталог сортов и цен за 1кг
CATALOG = {
    1: {"name": "Бленд Бразилия х Эфиопия 50/50", "price": 2750},
    2: {"name": "Эфиопия Сидамо", "price": 2800},
    3: {"name": "Колумбия Супремо", "price": 2980},
    4: {"name": "Бразилия Можиана", "price": 2870},
}

def show_catalog():
    """Показывает каталог сортов."""
    print("\n=== Каталог ===")
    for key, item in CATALOG.items():
        print(f"{key}. {item['name']} — {item['price']}₽/кг")
    print()

def get_discount(total_weight):
    """Считает скидку от общего веса."""
    if total_weight >= 10:
        return 20
    elif total_weight >= 6:
        return 10
    elif total_weight >= 3:
        return 5
    else:
        return 0

def main():
    print("Добро пожаловать в калькулятор скидок!")
    
    order = []  # список позиций заказа
    
    while True:
        show_catalog()
        
        # Выбор сорта
        try:
            choice = int(input("Выберите сорт (1-4): "))
            if choice not in CATALOG:
                print("Ошибка: выберите от 1 до 4.")
                continue
        except ValueError:
            print("Ошибка: введите число.")
            continue
        
        # Ввод веса
        try:
            weight = float(input("Введите вес (кг): "))
            if weight <= 0:
                print("Ошибка: вес должен быть больше 0.")
                continue
        except ValueError:
            print("Ошибка: введите число.")
            continue
        
        # Добавляем позицию
        item = CATALOG[choice]
        order.append({
            "name": item["name"],
            "price": item["price"],
            "weight": weight
        })
        
        # Спрашиваем про ещё один сорт
        answer = input("Добавить ещё сорт? (да/нет): ").strip().lower()
        if answer not in ["да", "yes", "y", "д"]:
            break
    
    # === Расчёт ===
    total_weight = sum(item["weight"] for item in order)
    total_sum = sum(item["price"] * item["weight"] for item in order)
    discount = get_discount(total_weight)
    discount_amount = total_sum * discount / 100
    final_sum = total_sum - discount_amount
    
    # === Вывод ===
    print("\n=== Ваш заказ ===")
    for i, item in enumerate(order, 1):
        item_sum = item["price"] * item["weight"]
        print(f"{i}. {item['name']} — {item['weight']}кг × {item['price']}₽ = {item_sum}₽")
    
    print(f"\nОбщий вес: {total_weight}кг")
    print(f"Сумма без скидки: {total_sum}₽")
    print(f"Скидка: {discount}%")
    print(f"Итоговая сумма: {final_sum}₽")
    print(f"Экономия: {discount_amount}₽")

if __name__ == "__main__":
    main()
