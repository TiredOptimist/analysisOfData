# Пароль считается надежным, если его длина составляет не менее 12 символов,
# при этом он должен содержать хотя бы одну заглавную букву, хотя бы одну строчную букву,
# хотя бы одну цифру и хотя бы один спецсимвол. Любые другие символы в пароле запрещены.
# Напишите программу, которая по указанному списку паролей определяет,
# какие из них являются надежными, а какие – нет.
# Допустимые заглавные буквы: ‘A’, ‘B’, …, ‘Z’ (все символы латинского алфавита).
# Допустимые строчные буквы: ‘a’, ‘b’, …, ‘z’ (все символы латинского алфавита).
# Допустимые спецсимволы: ‘!’, ‘@’, ‘#’, ‘$’, ‘%’, ‘&’, ‘*’, ‘+’.
n = int(input().strip())
passwords = [input().strip() for _ in range(n)]

special_chars = "!@#$%&*+"

for password in passwords:

    if len(password) < 12:
        print("Invalid")
        continue

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in special_chars:
            has_special = True

    if has_upper and has_lower and has_digit and has_special:
        print("Valid")
    else:
        print("Invalid")