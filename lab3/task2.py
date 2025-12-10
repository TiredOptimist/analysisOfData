import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve

# Загрузка данных
data = np.genfromtxt('data/data2.csv', delimiter=';', skip_header=1, dtype=float)
x = data[:, 0]  # Скидки
y = data[:, 1]  # Прибыль

print(f"Средняя прибыль по исходным данным: {np.mean(y):.2f}")

# Полином 2-й степени

# Выбор точек для квадратичного полинома
idx_quad = [0, len(x) // 2, -1]
x_quad = x[idx_quad]
y_quad = y[idx_quad]

# Матрица коэффициентов для квадратичного полинома
A_quad = np.array([
    [x_quad[0]**2, x_quad[0], 1],
    [x_quad[1]**2, x_quad[1], 1],
    [x_quad[2]**2, x_quad[2], 1]
])

# Решение системы уравнений
coeffs_quad = solve(A_quad, y_quad)

print("\nЗначения коэффициентов полинома 2-й степени")
print(coeffs_quad)

# Расчет значений полинома
y_pred_quad = coeffs_quad[0] * x**2 + coeffs_quad[1] * x + coeffs_quad[2]

# График для квадратичного полинома
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'o', label='Исходные данные')
plt.plot(x, y_pred_quad, '-', label='Полином 2-й степени')
plt.xlabel('Скидка')
plt.ylabel('Прибыль')
plt.legend()
plt.show()

# Расчет RSS
RSS_quad = np.sum((y - y_pred_quad) ** 2)
print("RSS для полинома 2-й степени:", RSS_quad)

# Полином 3-й степени

# Выбор точек для кубического полинома
idx_cubic = [0, len(x) // 3, 2 * len(x) // 3, -1]
x_cubic = x[idx_cubic]
y_cubic = y[idx_cubic]

# Матрица коэффициентов для кубического полинома
A_cubic = np.array([
    [x_cubic[0]**3, x_cubic[0]**2, x_cubic[0], 1],
    [x_cubic[1]**3, x_cubic[1]**2, x_cubic[1], 1],
    [x_cubic[2]**3, x_cubic[2]**2, x_cubic[2], 1],
    [x_cubic[3]**3, x_cubic[3]**2, x_cubic[3], 1]
])

# Решение системы уравнений
coeffs_cubic = solve(A_cubic, y_cubic)

print("\nЗначения коэффициентов полинома 3-й степени")
print(coeffs_cubic)

# Расчет значений полинома
y_pred_cubic = coeffs_cubic[0] * x**3 + coeffs_cubic[1] * x**2 + coeffs_cubic[2] * x + coeffs_cubic[3]

# График для кубического полинома
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'o', label='Исходные данные')
plt.plot(x, y_pred_cubic, '-', label='Полином 3-й степени')
plt.xlabel('Скидка')
plt.ylabel('Прибыль')
plt.legend()
plt.show()

# Расчет RSS
RSS_cubic = np.sum((y - y_pred_cubic) ** 2)
print("RSS для полинома 3-й степени:", RSS_cubic)

# Точки для прогноза
x_new = np.array([6, 8])

# Прогноз значений
y_pred_new = coeffs_cubic[0] * x_new**3 + coeffs_cubic[1] * x_new**2 + coeffs_cubic[2] * x_new + coeffs_cubic[3]

print("\nПрогноз прибыли для скидки 6% и 8%:", y_pred_new)


