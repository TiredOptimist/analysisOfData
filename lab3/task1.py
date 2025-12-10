import numpy as np

# Функция, которая заменяет некорректные данные на nan
def replace_unwanted_symbols(value):
    str_value = str(value)

    if str_value in ['--', 'ie', '']:
        return 'nan'

    return str_value


# 1. Загрузить информацию

arr_generation = np.array(
    np.genfromtxt('data/global-electricity-generation.csv', dtype=None, comments='#', delimiter=',', skip_header=1,
                  skip_footer=0, converters={i: replace_unwanted_symbols for i in range(31)}))
arr_consumption = np.array(
    np.genfromtxt('data/global-electricity-consumption.csv', dtype=None, comments='#', delimiter=',', skip_header=1,
                  skip_footer=0, converters={i: replace_unwanted_symbols for i in range(31)}))

# Массив названий стран из generation файла
arr_country_gen = []
for item in arr_generation:
    arr_country_gen.append(item[0])

# Массив названий стран из consumption файла
arr_country_con = []
for item in arr_consumption:
    arr_country_con.append(item[0])

if arr_country_gen == arr_country_con:
    print("Массивы названий стран идентичны - данные загружены корректно!")
else:
    print("Массивы названий стран различаются!")

# Преобразовываем значения в числовой формат
arr_generation = arr_generation[:, 1:].astype(float)
arr_consumption = arr_consumption[:, 1:].astype(float)

# 2. Построение массивов средних значений за последние 5 лет
last_five_years_generation = arr_generation[:, -5:]
last_five_years_consumption = arr_consumption[:, -5:]

# Вычисление средних значений (игнорируя nan)
avg_generation = np.array([
    np.nanmean(row) if not np.isnan(row).all() else np.nan
    for row in last_five_years_generation
])
avg_consumption = np.array([
    np.nanmean(row) if not np.isnan(row).all() else np.nan
    for row in last_five_years_consumption
])

print("\nСреднее производство электроэнергии за последние 5 лет по странам:")
for i in range(len(arr_country_gen)):
    if not np.isnan(avg_generation[i]):
        print(f"{arr_country_gen[i]}: {avg_generation[i]:.3f} млрд. кВт*ч")

print("\nСреднее потребление электроэнергии за последние 5 лет по странам:")
for i in range(len(arr_country_gen)):
    if not np.isnan(avg_consumption[i]):
        print(f"{arr_country_gen[i]}: {avg_consumption[i]:.3f} млрд. кВт*ч")

# 3. Ответы на вопросы

# 3.1. Суммарное (по всем странам) потребление электроэнергии за каждый год (игнорируя nan)
sum_consumption = np.nansum(arr_consumption, axis=0)
print("\nСуммарное (по всем странам) потребление электроэнергии за каждый год")
years = list(range(1992, 2022))
for i, year in enumerate(years):
    print(f"{year}: {sum_consumption[i]:.3f} млрд. кВт*ч")

# 3.2. Максимальное количество электроэнергии, которое произвела одна страна за один год (игнорируя nan)
max_generation_value = np.nanmax(arr_generation)
max_generation_indices = np.where(arr_generation == max_generation_value)
country_index = max_generation_indices[0][0]
year_index = max_generation_indices[1][0]
year = years[year_index]

print("\nМаксимальное количество электроэнергии, которое произвела одна страна за один год")
print(f"Страна: {arr_country_gen[country_index]}")
print(f"Год: {year}")
print(f"Производство: {max_generation_value:.3f} млрд. кВт*ч")

# 3.3. Список стран, которые производят более 500 млрд. кВт*ч электроэнергии ежегодно в среднем за последние 5 лет
print("\nСписок стран, которые производят более 500 млрд. кВт*ч электроэнергии ежегодно в среднем за последние 5 лет")
for i in range(len(avg_generation)):
    if not np.isnan(avg_generation[i]) and avg_generation[i] > 500:
        print(arr_country_gen[i])

# 3.4. 10% стран, которые потребляют больше всего электроэнергии ежегодно в среднем за последние 5 лет

print("\n10% стран, которые потребляют больше всего электроэнергии ежегодно в среднем за последние 5 лет ")
# Находим 90-й квантиль (игнорируя nan)
quantile_90 = np.nanquantile(avg_consumption, 0.90)

# Отбираем страны, которые превышают этот квантиль
for i in range(len(arr_country_gen)):
    if not np.isnan(avg_consumption[i]) and avg_consumption[i] > quantile_90:
        print(arr_country_gen[i])


# 3.5. Список стран, которые увеличили производство электроэнергии в 2021 году по сравнению с 1992 годом более, чем в 10 раз
print("\nСписок стран, которые увеличили производство электроэнергии в 2021 году по сравнению с 1992 годом более, чем в 10 раз")
generation_2021 = arr_generation[:, -1]
generation_1992 = arr_generation[:, 0]  # 1992 год - это первый столбец (индекс 0)
for i in range(len(arr_country_gen)):
    # Игнорируем случаи, где есть nan значения
    if not np.isnan(generation_1992[i]) and not np.isnan(generation_2021[i]):
        if generation_1992[i] != 0 and generation_2021[i] > 10 * generation_1992[i]:
            print(arr_country_gen[i])

# 3.6. Список стран, которые в сумме за все годы потратили больше 100 млрд. кВт*ч электроэнергии и при этом произвели меньше, чем потратили
print("\nСписок стран, которые в сумме за все годы потратили больше 100 млрд. кВт*ч электроэнергии и при этом произвели меньше, чем потратили")

# Потребление энергии каждой страной за все годы (игнорируя nan)
sum_consumption_all = np.nansum(arr_consumption, axis=1)

# Производство энергии каждой страной за все годы (игнорируя nan)
sum_generation_all = np.nansum(arr_generation, axis=1)

for i in range(len(sum_generation_all)):
    if not np.isnan(sum_consumption_all[i]) and not np.isnan(sum_generation_all[i]):
        if sum_consumption_all[i] > 100 and sum_generation_all[i] < sum_consumption_all[i]:
            print(arr_country_gen[i])


# 3.7. Какая страна потратила наибольшее количество электроэнергии в 2020 году?
print("\nКакая страна потратила наибольшее количество электроэнергии в 2020 году?")
max_consumption_index = np.nanargmax(arr_consumption[:, -2])  # индекс максимального потребления в 2020
print(arr_country_gen[max_consumption_index])
