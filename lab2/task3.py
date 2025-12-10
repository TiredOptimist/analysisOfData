# Ваша задача – по имеющимся записям о посещаемости одной группы определить,
# какая доля всех записей является некорректной.
# Некорректными мы будем считать данные, которые сильно отличаются от остальных
# (в статистике это называется выбросами).
# Более точно алгоритм выглядит так. Пусть у нас есть набор данных, состоящий из N значений.
# Вначале найдём квартили для этого набора (Q1, Q2, Q3).
# Затем определим разброс квартилей IQR = Q3 - Q1. Выбросами (некорректными данными)
# будем считать все значения, которые меньше, чем Q1-1.5*IQR, а также все значения,
# которые больше, чем Q3+1.5*IQR.

n = int(input().strip())
data = [int(input().strip()) for _ in range(n)]

sorted_data = sorted(data)

def find_median(arr):
    n_arr = len(arr)
    if n_arr % 2 == 1:
        return arr[n_arr // 2]
    else:
        return (arr[n_arr // 2 - 1] + arr[n_arr // 2]) / 2

q2 = find_median(sorted_data)

if n % 2 == 1:
    lower_half = sorted_data[:n // 2]
    upper_half = sorted_data[n // 2 + 1:]
else:
    lower_half = sorted_data[:n // 2]
    upper_half = sorted_data[n // 2:]

q1 = find_median(lower_half)
q3 = find_median(upper_half)

iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outliers = 0
for value in data:
    if value < lower_bound or value > upper_bound:
        outliers += 1

print(outliers)
