# -*- coding: utf-8 -*-
"""ML6_3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GKWMMPOrAbYE6NmPi00vVeBcbYKQftlT

##Задания для самостоятельного выполнения
"""

import pandas as pd

"""#### 1. Загрузите прилагающийся датасет credit_data.

"""

data = pd.read_csv('credit_data.csv')

data_info = data.info()
data_head = data.head()

data_info, data_head

"""#### 2. Проверьте датасет на наличие текстовых атрибутов. Замените текстовые атрибуты на числовые без потери качества данных.

"""

# Преобразование категориальных признаков в числовые
data['Sex'] = data['Sex'].map({'male': 0, 'female': 1})
data['Housing'] = data['Housing'].map({'own': 0, 'rent': 1, 'free': 2})
data['Saving accounts'] = data['Saving accounts'].map({'little': 1, 'moderate': 2, 'quite rich': 3, 'rich': 4})
data['Checking account'] = data['Checking account'].map({'little': 1, 'moderate': 2, 'rich': 3})
data['Risk'] = data['Risk'].map({'good': 1, 'bad': 0})

# Замена пропущенных значений на 0
data['Saving accounts'] = data['Saving accounts'].fillna(0)
data['Checking account'] = data['Checking account'].fillna(0)

# Удаление ненужных столбцов
target = data['Risk']
data = data.drop(['Risk', 'Unnamed: 0', 'Purpose'], axis=1)

data.head()

"""####3. Выведите информацию о количественных параметрах датасета;

"""

print(data.describe())

"""####4. Разделите эти данные на тестовую и обучающую выборки;

"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.3, random_state=42)

"""####5. Обучите модель случайных лесов на обучающей выборке. Проверьте точность предсказаний.

"""

from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
print("Precision:", metrics.precision_score(y_test, y_pred))
print("Recall:", metrics.recall_score(y_test, y_pred))
print("F1 Score:", metrics.f1_score(y_test, y_pred))

"""####7. Понизьте размерность данных с помощью метода главных компонент.


"""

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Нормализация данных
scaler = StandardScaler()
X_scaled = scaler.fit_transform(data)

# Понижение размерности методом PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
print(X_pca.shape)

"""####8. Обучите заново модель случайных лесов и оцените ее эффективность с помощью метрик.


"""

X_train_pca, X_test_pca, y_train_pca, y_test_pca = train_test_split(X_pca, target, test_size=0.3, random_state=42)

clf_pca = RandomForestClassifier(n_estimators=100, random_state=42)
clf_pca.fit(X_train_pca, y_train_pca)

y_pred_pca = clf_pca.predict(X_test_pca)
print("Accuracy after PCA:", metrics.accuracy_score(y_test_pca, y_pred_pca))
print("Precision after PCA:", metrics.precision_score(y_test_pca, y_pred_pca))
print("Recall after PCA:", metrics.recall_score(y_test_pca, y_pred_pca))
print("F1 Score after PCA:", metrics.f1_score(y_test_pca, y_pred_pca))

"""####9. Постройте график зависимости точности модели от размерности данных.


"""

import numpy as np
import matplotlib.pyplot as plt

# Определение диапазона размерностей
dimensions = np.arange(1, data.shape[1] + 1)
accuracies = []

for dim in dimensions:
    pca = PCA(n_components=dim)
    X_pca = pca.fit_transform(X_scaled)
    X_train_pca, X_test_pca, y_train_pca, y_test_pca = train_test_split(X_pca, target, test_size=0.3, random_state=42)
    clf_pca.fit(X_train_pca, y_train_pca)
    y_pred_pca = clf_pca.predict(X_test_pca)
    accuracies.append(metrics.accuracy_score(y_test_pca, y_pred_pca))

plt.plot(dimensions, accuracies, marker='o')
plt.title('Зависимость точности модели от размерности данных')
plt.xlabel('Количество главных компонент')
plt.ylabel('Точность')
plt.grid(True)
plt.show()

"""####10. Сделайте вывод о применимости модели.

Модель случайных лесов показала снижение точности после понижения размерности данных. Это указывает на то, что метод PCA может не всегда улучшать результаты классификации и требует тщательной настройки и анализа данных для достижения наилучших результатов.
"""