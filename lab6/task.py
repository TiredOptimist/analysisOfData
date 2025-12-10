import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

# 1. Загрузите данные из файла "boston.csv"
# о недвижимости в различных районах Бостона.
data = pd.read_csv("boston.csv")

# 2. Проверьте, что у всех загруженных данных числовой тип.
print("Типы данных\n")
print(data.dtypes)

# 3. Проверьте, есть ли по каким-либо признакам отсутствующие данные.
# Если отсутствующие данные есть – заполните их медианным значением.
print("\nКоличество отсутствующих данных в каждом столбце:\n")
print(data.isnull().sum())
if data.isnull().values.any():
    # Заполнение пропущенных значений медианой
    # если True, будет изменять исходный DataFrame.
    data.fillna(data.median(), inplace=True)

# 4. Посчитайте коэффициент корреляции для всех пар признаков.
# Подсказка: воспользуйтесь методом corr() для датафрейма,
# чтобы получить сразу всю корреляционную матрицу.
corr_matrix = data.corr()
print("\nКоэффициент корреляции для всех пар признаков:\n")
print(corr_matrix)

# 5. С помощью одной из библиотек визуализации постройте тепловую
# карту (heatmap) по корреляционной матрице.
plt.figure(figsize=(12, 12))
# Annot=True: значения в ячейках тепловой карты должны быть отображены на самой карте.
# Coolwarm — палитра в seaborn, которая отображает значения от холодных (синих) к теплым (красным) цветам.
sns.heatmap(corr_matrix, annot=True, fmt=".1f", cmap='coolwarm')
plt.title('Тепловая карта по корреляционной матрице')
plt.show()

# 6. Выберите от 4 до 6 признаков (на свое усмотрение), которые в наибольшей
# степени коррелируют с целевым признаком (ценой недвижимости). Справка.
# Коэффициент корреляции изменяется от -1 до 1, Значение -1 означает точную
# обратно-пропорциональную зависимость (чем меньше одна переменная, тем больше вторая, и наоборот).
# Значение 1 означает точную прямо-пропорциональную зависимость. Значение 0 означает полное
# отсутствие зависимости. Таким образом, чем ближе модуль коэффициента корреляции к 1,
# тем сильнее прослеживается зависимость между признаками.
# MEDV – медианная цена недвижимости (тыс. $) – целевой признак
target = 'MEDV'
#  ascending=False сортировка по убыванию
# выбираем индексы с 1 по 5, чтобы исключить первый индекс (который соответствует
# самой целевой переменной target, так как корреляция с самой собой всегда равна 1)
priznaks = corr_matrix[target].abs().sort_values(ascending=False).index[1:6]  # выбираем 5 признаков
print("Выбранные признаки:", priznaks)

# 7. Для каждого из выбранных признаков в паре с целевым признаком
# постройте точечную диаграмму (диаграмму рассеяния).
for priznak in priznaks:
    plt.figure(figsize=(8, 8))
    # по оси X будут отложены значения текущего признака
    # по оси Y будут отложены значения целевой переменной
    sns.scatterplot(x=data[priznak], y=data[target])
    plt.title(f'Диаграмма рассеяния: {priznak} vs {target}')
    plt.xlabel(priznak)
    plt.ylabel(target)
    plt.show()

# 8. Визуально убедитесь, что связь между выбранным признаком и
# целевым прослеживается. Если на основе графика считаете, что зависимости
# нет – исключите этот признак из дальнейшего рассмотрения (но при этом как
# минимум 3 признака должно остаться в любом случае).
priznaks = priznaks[0:3]
print("\nОставленные признаки:", priznaks)

# 9. Сформируйте список факторных признаков и целевую переменную.
X = data[list(priznaks)]
y = data[target]
print("Список факторных признаков:\n", X)
print("Целевая переменная:\n", y)

# 10. Выполните разбиение датасета на обучающую и тестовую выборки в соотношении 8:2.
# При формировании обучающей и тестовой выборок строки из исходного датафрейма должны
# выбираться в случайном порядке. Подсказка: можно воспользоваться функцией train_test_split
# из библиотеки sklearn.model_selection.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=30)

# 11. Из набора линейных моделей библиотеки sklearn возьмите
# линейную регрессию, обучите ее на обучающем наборе.
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)

# 12. Получите векторы прогнозных значений целевой переменной на обучающей и на тестовой выборках.
y_train_pred = lin_reg.predict(X_train)
y_test_pred = lin_reg.predict(X_test)

# 13. Посчитайте коэффициент детерминации (R2) и корень из
# среднеквадратичной ошибки (RMSE) на обучающей и на тестовой выборках.
# Функция r2_score вычисляет коэффициент детерминации (R²), который показывает,
# какую долю дисперсии целевой переменной объясняет модель.
# RMSE — это метрика, оценивающая точность регрессии, чем меньше, тем лучше
# y_train — это истинные значения целевой переменной для обучающего набора данных.
# y_train_pred — это предсказанные значения, которые были получены моделью на том же наборе данных.
r2_train = r2_score(y_train, y_train_pred)
rmse_train = np.sqrt(mean_squared_error(y_train, y_train_pred))
r2_test = r2_score(y_test, y_test_pred)
rmse_test = np.sqrt(mean_squared_error(y_test, y_test_pred))

print(f'Обучающая выборка: R2 = {r2_train:}, RMSE = {rmse_train:}')
print(f'Тестовая выборка: R2 = {r2_test:}, RMSE = {rmse_test:}')

# 14. Постройте boxplot («ящик с усами») для целевого признака (MEDV).
# Определите, какие значения можно считать выбросами. Указание.
# Если по диаграмме выбросы определить не смогли, то для выполнения
# дальнейших действий считайте выбросами значения MEDV=50.0.
plt.figure(figsize=(8, 8))
sns.boxplot(y=data[target])
plt.title('Boxplot для MEDV')
plt.show()

# Определение выбросов
outs = data[(data[target] < 5.5) | (data[target] > 36.5)]
print("Выбросы:\n", outs)

# 15. Отфильтруйте исходные данные, удалив выбросы. Пересоздайте тестовую и обучающую выборки, переобучите модель.
# Посчитайте показатели R2 и RMSE. Как они изменились? О чем это говорит?
# Фильтруем данные
data_filtered = data[(data[target] > 5.5) & (data[target] < 36.5)]

# Формируем список факторных признаков и целевую переменную
X_filtered = data_filtered[list(priznaks)]
y_filtered = data_filtered[target]

# Разбиение датасета на обучающую и тестовую выборки
X_train_filt, X_test_filt, y_train_filt, y_test_filt = train_test_split(X_filtered, y_filtered, test_size=0.2, random_state=30)

# Линейная регрессия и обучение на новом наборе
lin_reg.fit(X_train_filt, y_train_filt)

# Векторы прогнозных значений целевой переменной на обучающей и на тестовой выборках (новых)
y_train_filt_pred = lin_reg.predict(X_train_filt)
y_test_filt_pred = lin_reg.predict(X_test_filt)

# Коэффициент детерминации (R2) и корень из среднеквадратичной ошибки (RMSE) на обучающей и на тестовой выборках.
# y_train_filt — это истинные значения целевой переменной для обучающего набора данных.
# y_train_filt_pred — это предсказанные значения, которые были получены моделью на том же наборе данных.
r2_train_filt = r2_score(y_train_filt, y_train_filt_pred)
rmse_train_filt = np.sqrt(mean_squared_error(y_train_filt, y_train_filt_pred))
r2_test_filt = r2_score(y_test_filt, y_test_filt_pred)
rmse_test_filt = np.sqrt(mean_squared_error(y_test_filt, y_test_filt_pred))

print("\nСравнение моделей до и после удаления выбросов")
print(f"R2 (тест до): {r2_test:.4f},  R2 (тест после): {r2_test_filt:.4f}")
print(f"RMSE (тест до): {rmse_test:.4f},  RMSE (тест после): {rmse_test_filt:.4f}")

print("\nВывод:")
if r2_test_filt > r2_test and rmse_test_filt < rmse_test:
    print("После удаления выбросов качество модели улучшилось: R² увеличился, RMSE уменьшился.")
elif r2_test_filt < r2_test and rmse_test_filt > rmse_test:
    print("После удаления выбросов качество модели ухудшилось: R² уменьшился, RMSE увеличился.")
else:
    print("После удаления выбросов качество модели изменилось незначительно.")

# 16. Из набора линейных моделей библиотеки sklearn возьмите гребневую регрессию (Ridge).
# Обучите модель. Посчитайте показатели R2 и RMSE.
# Обучаем модель с гребневой регрессией на обучающем наборе
ridge_reg = Ridge()
ridge_reg.fit(X_train_filt, y_train_filt)

# Векторы прогнозных значений целевой переменной
y_train_ridge_pred = ridge_reg.predict(X_train_filt)
y_test_ridge_pred = ridge_reg.predict(X_test_filt)

# Линейная регрессия с регуляризацией для борьбы с переобучением
# Коэффициент детерминации (R2) и корень из среднеквадратичной ошибки (RMSE) на обучающей и на тестовой выборках.
# y_train_filt — это истинные значения целевой переменной для обучающего набора данных.
# y_train_ridge_pred — это предсказанные значения, которые были получены моделью на том же наборе данных.
r2_train_ridge = r2_score(y_train_filt, y_train_ridge_pred)
rmse_train_ridge = np.sqrt(mean_squared_error(y_train_filt, y_train_ridge_pred))
r2_test_ridge = r2_score(y_test_filt, y_test_ridge_pred)
rmse_test_ridge = np.sqrt(mean_squared_error(y_test_filt, y_test_ridge_pred))

print(f'\nГребневая регрессия - Обучающая выборка: R2 = {r2_train_ridge:}, RMSE = {rmse_train_ridge:}')
print(f'Гребневая регрессия - Тестовая выборка: R2 = {r2_test_ridge:}, RMSE = {rmse_test_ridge:}')

# 17. Постройте полиномиальную регрессию с использованием полинома 3-й степени.
# Посчитайте показатели R2 и RMSE. Сравните все полученные результаты.
# Преобразование исходных признаков в полиномиальные
# Полином 3-й степени degree=3
poly_reg = PolynomialFeatures(degree=3)
X_poly = poly_reg.fit_transform(X_filtered)

X_train_poly, X_test_poly, y_train_poly, y_test_poly = train_test_split(X_poly, y_filtered, test_size=0.2, random_state=30)

# Обучение модели полиномиальной регрессии
lin_reg.fit(X_train_poly, y_train_poly)

# Векторы прогнозных значений целевой переменной
y_train_poly_pred = lin_reg.predict(X_train_poly)
y_test_poly_pred = lin_reg.predict(X_test_poly)

# Коэффициент детерминации (R2) и корень из среднеквадратичной ошибки (RMSE) на обучающей и на тестовой выборках.
# y_train_filt — это истинные значения целевой переменной для обучающего набора данных.
# y_train_poly_pred — это предсказанные значения, которые были получены моделью на том же наборе данных.
r2_train_poly = r2_score(y_train_poly, y_train_poly_pred)
rmse_train_poly = np.sqrt(mean_squared_error(y_train_poly, y_train_poly_pred))
r2_test_poly = r2_score(y_test_poly, y_test_poly_pred)
rmse_test_poly = np.sqrt(mean_squared_error(y_test_poly, y_test_poly_pred))

print(f'\nПолиномиальная регрессия - Обучающая выборка: R2 = {r2_train_poly:}, RMSE = {rmse_train_poly:}')
print(f'Полиномиальная регрессия - Тестовая выборка: R2 = {r2_test_poly:}, RMSE = {rmse_test_poly:}')

# Сравнение моделей

# Создаем таблицу сравнения моделей
print("\nСравнение моделей после удаления выбросов:\n")
print(f"{'Модель':<25}{'R2 train':<12}{'RMSE train':<12}{'R2 test':<12}{'RMSE test':<12}")
print("-" * 73)
print(f"{'Линейная регрессия':<25}{r2_train_filt:<12.4f}{rmse_train_filt:<12.4f}{r2_test_filt:<12.4f}{rmse_test_filt:<12.4f}")
print(f"{'Гребневая регрессия':<25}{r2_train_ridge:<12.4f}{rmse_train_ridge:<12.4f}{r2_test_ridge:<12.4f}{rmse_test_ridge:<12.4f}")
print(f"{'Полиномиальная регрессия':<25}{r2_train_poly:<12.4f}{rmse_train_poly:<12.4f}{r2_test_poly:<12.4f}{rmse_test_poly:<12.4f}")

# Выводим вывод о лучшей модели
print("\nВывод:")
best_model = ''
if r2_test_poly > r2_test_ridge and r2_test_poly > r2_test_filt:
    best_model = 'Полиномиальная регрессия'
elif r2_test_ridge > r2_test_filt:
    best_model = 'Гребневая регрессия'
else:
    best_model = 'Линейная регрессия'

print(f"Лучшая модель: {best_model}.")
