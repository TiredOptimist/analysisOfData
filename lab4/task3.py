import pandas as pd
import os

# 1. Загрузка данных с проверкой наличия файлов
if os.path.exists('telecom_churn.csv'):
    data = pd.read_csv('telecom_churn.csv')
else:
    print("Файл 'telecom_churn.csv' не найден.")

# 2. Выведите общую информацию о датафрейме с помощью методов info или describe. Есть ли отсутствующие данные?
print(data.info())

# Проверка на наличие отсутствующих данных
not_values = data.isnull().sum()  # Считаем количество пропущенных значений в каждом столбце
print("\nОтсутствующие данные:")
print(not_values[not_values > 0])

# 2. С помощью метода value_counts определите, сколько клиентов активны, а сколько потеряно.
# Сколько процентов клиентов в имеющихся данных активны, а сколько потеряны?
# Churn – отток клиентов (False – клиент активен, true – клиент потерян, то есть расторг договор)
val_counts = data['Churn'].value_counts()
print("\nКоличество клиентов:\n", val_counts)


# Процент активных и потерянных клиентов
active = val_counts[False] / val_counts.sum() * 100
lost = val_counts[True] / val_counts.sum() * 100
print(f"Процент активных клиентов: {active:.2f}%")
print(f"Процент потерянных клиентов: {lost:.2f}%")

# 3. Добавьте дополнительный столбец в датафрейм продолжительность одного звонка
# (вычислить как суммарная продолжительность всех звонков, деленная на суммарное количество всех звонков).
# Отсортируйте данные по этому значению по убыванию и выведите 10 первых записей.
data['Duration of one call'] = (
        (data['Total day minutes'] + data['Total eve minutes'] + data['Total night minutes']) /
        (data['Total day calls'] + data['Total eve calls'] + data['Total night calls'])
)

# Сортировка по убыванию и вывод первых 10 записей
sorted_data = data.sort_values(by='Duration of one call', ascending=False)
print('\n10 первых записей продолжительности одного звонка')
print(sorted_data[['Duration of one call']].head(10))

# 4. Сгруппируйте данные по значению поля «Churn» и вычислите среднюю продолжительность одного звонка
# в каждой категории. Есть ли существенная разница в средней продолжительности одного звонка
# между активными и потерянными клиентами?
av_duration = data.groupby('Churn')['Duration of one call'].mean()
print("\nСредняя продолжительность одного звонка по категориям Churn:\n", av_duration)
print('Существенной разницы в средней продолжительности одного звонка между активными и потерянными клиентами нет\n')

# 5. Сгруппируйте данные по значению поля «Churn» и вычислите среднее количество звонков в службу поддержки
# в каждой категории. Есть ли существенная разница между активными и потерянными клиентами?
av_service = data.groupby('Churn')['Customer service calls'].mean()
print("\nСреднее количество звонков в службу поддержки по категориям Churn:\n", av_service)
print('Имеется довольно существенная разница в среднем количестве звонков в службу поддержки между активными и '
      'потерянными клиентами\n')

# 6. Исследуйте подробнее связь между параметрами «Churn» и «Customer service calls»,
# построив таблицу сопряженности (факторную таблицу) по этим признакам.
# Подсказка: используйте функцию crosstab. При каком количестве звонков в службу поддержки процент
# оттока становится существенно выше, чем в целом по датафрейму? (В качестве уточнения фразы «существенно выше»
# можете использовать «более 40%».)
crosstab_calls = pd.crosstab(data['Customer service calls'], data['Churn'])
print("\nТаблица сопряженности между Churn и Customer service calls:\n", crosstab_calls)

# Процент оттока для каждого значения "Customer service calls"
# axis=1 указывает, что сумма должна быть рассчитана по строкам
crosstab_calls['Churn rate'] = crosstab_calls[True] / crosstab_calls.sum(axis=1) * 100

# Определение порога, при котором процент оттока выше 40%
high_churn = crosstab_calls[crosstab_calls['Churn rate'] > 40]
print("\nКоличество звонков в службу поддержки при проценте оттока выше 40%:\n", high_churn)

# 7. Аналогично предыдущему пункту исследуйте связь между параметрами «Churn» и «International plan».
# Можно ли утверждать, что процент оттока среди клиентов, использующих международный роуминг, существенно
# выше или ниже, чем среди клиентов, не использующих его?
crosstab_plan = pd.crosstab(data['International plan'], data['Churn'])
print("\nТаблица сопряженности между Churn и International plan:\n", crosstab_plan)

# Процент оттока для каждого значения "International plan"
# axis=1 указывает, что сумма должна быть рассчитана по строкам
# Количество оттока делим на всех, кто использует/не использует роуминг (No 3010, Yes 323)
crosstab_plan['Churn rate'] = crosstab_plan[True] / crosstab_plan.sum(axis=1) * 100
print("\nПроцент оттока по наличию международного роуминга:\n", crosstab_plan[['Churn rate']])
print('У людей, у которых не подключена услуга международного роуминга, процент оттока ниже, чем у людей, у которых '
      'подключена эта услуга')

# 8. Добавьте в датафрейм столбец «Прогнозируемый отток», заполнив его на основе значений столбцов
# «Customer service calls» и «International plan».
# Сравните значение в этом столбце со значением столбца «Churn». Если мы будем пользоваться построенным прогнозом,
# то какой процент ошибок первого и второго рода (ложноположительных и ложноотрицательных) мы получим?
data['Projected Churn'] = ((data['Customer service calls'] >= 4) | (data['International plan'] == 'Yes')).astype(bool)

# Сравнение значений столбца "Predicted Churn" со столбцом "Churn"
true_true = ((data['Projected Churn'] == True) & (data['Churn'] == True)).sum()
true_false = ((data['Projected Churn'] == True) & (data['Churn'] == False)).sum()
false_false = ((data['Projected Churn'] == False) & (data['Churn'] == False)).sum()
false_true = ((data['Projected Churn'] == False) & (data['Churn'] == True)).sum()

total_predictions = len(data)
error_1 = true_false / total_predictions * 100
print('\nПроцент ошибок первого рода', error_1)
error_2 = false_true / total_predictions * 100
print('Процент ошибок второго рода', error_2)
