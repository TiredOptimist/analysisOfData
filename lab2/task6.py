# Файл mbox.txt содержит метаданные почтового сервера.
# Мы знаем, что строка с адресом автора письма начинается с "From ".
# Найти адреса всех авторов сообщений и найти того из них, кто пишет больше всех писем.

from collections import defaultdict

try:
    with open('analysisOfData/lab2/mbox.txt', 'r', encoding='utf-8') as file:
        email_count = defaultdict(int)

        for line in file:
            # Ищем строки, начинающиеся с "From "
            if line.startswith('From '):
                words = line.split()
                if len(words) >= 2:
                    email = words[1]
                    email_count[email] += 1

        # Проверяем, найдены ли письма
        if email_count:
            # Находим самого активного отправителя
            max_sender = max(email_count, key=email_count.get)
            max_count = email_count[max_sender]

            print("Результат: ")
            print(f"Найдено писем: {sum(email_count.values())}")
            print(f"Уникальных отправителей: {len(email_count)}")

            print("Топ-5 самых активных отправителей:")
            sorted_senders = sorted(email_count.items(), key=lambda x: x[1], reverse=True)[:5]

            for i, (email, count) in enumerate(sorted_senders, 1):
                print(f"{i}. {email} - {count} писем")

            print(f"Самый активный отправитель:")
            print(f"Email: {max_sender}")
            print(f"Количество писем: {max_count}")

        else:
            print("В файле не найдено ни одного письма!")

except FileNotFoundError:
    print("ОШИБКА: Файл mbox.txt не найден!")

except Exception as e:
    print(f"Произошла ошибка при чтении файла: {e}")