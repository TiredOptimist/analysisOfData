# Напишите программу, которая будет выводить:
# а) список всех пицц с указанием, сколько раз их заказывали; список должен быть отсортирован по убыванию количества заказов, то есть первой в списке должна оказаться самая популярная пицца;
# б) список всех дат с указанием суммарной стоимости проданных в этот день пицц; список должен быть отсортирован хронологически;
# в) информацию о самом дорогом заказе;
# г) среднюю стоимость заказа (среднее арифметическое по всем стоимостям).
# Формат входных и выходных данных определите самостоятельно.

from datetime import datetime
from collections import defaultdict

orders = []

print("Введите заказы (формат: ДД.ММ.ГГГГ Пицца Цена):")
print("Пример: 15.05.2023 Пепперони 850.50")
print("Для завершения ввода введите 'стоп'")

while True:
    line = input().strip()

    if line.lower() == 'стоп':
        break
    if not line:
        continue

    try:
        parts = line.split()
        if len(parts) < 3:
            print(f"Ошибка: некорректный формат строки '{line}'")
            continue

        date_str = parts[0]
        cost_str = parts[-1]
        pizza_name = ' '.join(parts[1:-1])

        date = datetime.strptime(date_str, '%d.%m.%Y')
        cost = float(cost_str)

        if cost <= 0:
            print(f"Ошибка: стоимость должна быть положительной - '{line}'")
            continue

        orders.append({'date': date, 'pizza': pizza_name, 'cost': cost})

    except ValueError:
        print(f"Ошибка в формате данных: '{line}'")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

if not orders:
    print("Не введено ни одного заказа!")
else:
    # а) Статистика по пиццам
    pizza_count = defaultdict(int)
    for order in orders:
        pizza_count[order['pizza']] += 1

    print("\nа) Популярность пицц (по убыванию):")
    sorted_pizzas = sorted(pizza_count.items(), key=lambda x: (-x[1], x[0]))
    for pizza, count in sorted_pizzas:
        print(f"{pizza}: {count}")

    # б) Статистика по датам
    date_total = defaultdict(float)
    for order in orders:
        date_str = order['date'].strftime('%d.%m.%Y')
        date_total[date_str] += order['cost']

    print("\nб) Выручка по дням (хронологически):")
    sorted_dates = sorted(date_total.items(),
                          key=lambda x: datetime.strptime(x[0], '%d.%m.%Y'))
    for date, total in sorted_dates:
        print(f"{date}: {total:.2f} руб.")

    # в) Самый дорогой заказ
    expensive = max(orders, key=lambda x: x['cost'])
    print(f"\nв) Самый дорогой заказ:")
    print(f"Дата: {expensive['date'].strftime('%d.%m.%Y')}")
    print(f"Пицца: {expensive['pizza']}")
    print(f"Стоимость: {expensive['cost']:.2f} руб.")

    # г) Средняя стоимость
    avg_cost = sum(order['cost'] for order in orders) / len(orders)
    print(f"\nг) Средняя стоимость заказа: {avg_cost:.2f} руб.")