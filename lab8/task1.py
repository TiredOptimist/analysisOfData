import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

# Загружаем данные
df = pd.read_csv("27_B_17834.csv", sep=';')

# Преобразуем строки с координатами X и Y из строкового формата с запятой в вещественные числа
df['X'] = df['X'].str.replace(",", ".").astype(float)
df['Y'] = df['Y'].str.replace(",", ".").astype(float)

# Кластеризация KMeans (минимизации расстояния между объектами внутри одного кластера) на 3 кластера

# KMeans — алгоритм кластеризации, который делит точки на заданное число кластеров так,
# чтобы каждая точка была ближе к центру своего кластера, чем к центрам других.
# n_clusters=3 — число кластеров
model = KMeans(n_clusters=3, random_state=0)
df['Cluster'] = model.fit_predict(df[['X', 'Y']]) # обучаем модель и присваиваем каждой точке номер кластера

# Находим реальные центроиды по определению задачи

real_centroids = []

for cluster in sorted(df['Cluster'].unique()):
    # Берём все точки кластера
    cluster_points = df[df['Cluster'] == cluster][['X', 'Y']].values

    # Считаем евклидовы расстояния между каждой парой точек внутри кластера и получаем матрицу расстояний
    distances = cdist(cluster_points, cluster_points, 'euclidean')

    # Суммируем расстояния от каждой точки до остальных
    sums = distances.sum(axis=1)

    # Точка с минимальной суммой расстояний — реальный центроид
    centroid = cluster_points[np.argmin(sums)]
    real_centroids.append(centroid)

# Преобразуем в массив numpy
real_centroids = np.array(real_centroids)

plt.figure(figsize=(6, 6))
plt.scatter(df['X'], df['Y'], c=df['Cluster'], alpha=0.3, marker='.')
plt.scatter(real_centroids[:, 0], real_centroids[:, 1], c='r', s=150, marker='.', label='Центроиды')
plt.title('Центроиды кластеров на данных')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.show()

for i, c in enumerate(real_centroids):
    print(f"Кластер {i + 1}: центроид ({c[0]:.3f}, {c[1]:.3f})")
