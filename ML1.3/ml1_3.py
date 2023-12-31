# -*- coding: utf-8 -*-
"""ML1.3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xwSaJpVOG9rL5xTX7GZQveW63Ho8zL02

##Методические указания
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.datasets import fetch_california_housing
california = fetch_california_housing()

type(california)

california.keys()

print(type(california.data), type(california.target))

print(california.data.shape, california.target.shape)

data = pd.DataFrame(california.data, columns = california.feature_names)
data['Price'] = california.target
data.head()

data.info()

data.describe().round(2)

y = data['Price']
X = data.drop('Price', axis=1)

y.shape, X.shape

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X, y)

print("Coefficients: \n", model.coef_)

_ = [print(k, v) for k, v in zip(X.columns, model.coef_)]

print("Intercept: \n", model.intercept_)

y_pred = model.predict(X)
print(y_pred[:5])

print(y[:5])

plt.scatter(y_pred, y)
plt.plot(y, y, c='r')

model.score(X, y)

from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(5).fit_transform(X)

polynomial = LinearRegression()
polynomial.fit(poly, y)
y_pred_poly = polynomial.predict(poly)

plt.scatter(y_pred_poly, y)
plt.plot(y, y, c='r')

polynomial.score(poly, y)

"""##Задания для самостоятельного выполнения

###Задание №1

Кросс-валидация
"""

from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')
# Можно вывести среднее значение MSE
mean_mse = -scores.mean()
print(f'Среднее MSE: {mean_mse}')

"""Оценка остатков"""

residuals = y - y_pred

plt.figure(figsize=(8, 6))
plt.hist(residuals, bins=30, color='pink', edgecolor='gray')
plt.title('Гистограмма остатков')
plt.xlabel('Остатки')
plt.ylabel('Частота')
plt.grid(True, linestyle='--', alpha=0.7)


plt.show()

"""Регуляризация"""

from sklearn.linear_model import Lasso, Ridge
lasso_model = Lasso(alpha=0.01)  # Подбираем оптимальное значение alpha
lasso_model.fit(X, y)

lasso_score = lasso_model.score(X, y)
print(f'Lasso R^2 Score: {lasso_score}')

"""Подбор параметров"""

from sklearn.model_selection import GridSearchCV
param_grid = {'alpha': [0.01, 0.1, 1, 10, 100]}
grid_search = GridSearchCV(Lasso(), param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X, y)
best_alpha = grid_search.best_params_['alpha']
print(f'Best Alpha: {best_alpha}')

"""###Задание №2

####Метод опорных векторов

a. Без ядра
"""

from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9, random_state=42)

svm_model = SVR(kernel='linear', epsilon=0.9)

svm_model.fit(X_train, y_train)

y_pred_svm = svm_model.predict(X_test)

r2_svm = r2_score(y_test, y_pred_svm)
print(f'Оценка R^2 модели SVM без ядра: {r2_svm}')

plt.scatter(y_test, y_pred_svm)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Реальные значения')
plt.ylabel('Предсказанные значения')
plt.title('Визуализация регрессии (SVM без ядра)')
plt.show()

"""b. С гауссовым ядром"""

from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score


svm_rbf_model = SVR(kernel='rbf')

svm_rbf_model.fit(X_train, y_train)

y_pred_svm_rbf = svm_rbf_model.predict(X_test)

r2_svm_rbf = r2_score(y_test, y_pred_svm_rbf)
print(f'Оценка R^2 модели SVM с гауссовым ядром (RBF): {r2_svm_rbf}')

plt.scatter(y_test, y_pred_svm_rbf)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Реальные значения')
plt.ylabel('Предсказанные значения')
plt.title('Визуализация регрессии (SVM с гауссовым ядром)')
plt.show()

"""c. С полиномиальным ядром"""

svm_poly_model = SVR(kernel='poly', degree=3)

svm_poly_model.fit(X_train, y_train)

y_pred_svm_poly = svm_poly_model.predict(X_test)

r2_svm_poly = r2_score(y_test, y_pred_svm_poly)
print(f'Оценка R^2 модели SVM с полиномиальным ядром: {r2_svm_poly}')

plt.scatter(y_test, y_pred_svm_poly)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Реальные значения')
plt.ylabel('Предсказанные значения')
plt.title('Визуализация регрессии (SVM с полиномиальным ядром)')
plt.show()

"""####Метод ближайших соседей"""

from sklearn.neighbors import KNeighborsRegressor

knn_model = KNeighborsRegressor(n_neighbors=5)

knn_model.fit(X_train, y_train)

y_pred_knn = knn_model.predict(X_test)

r2_knn = r2_score(y_test, y_pred_knn)
print(f'Оценка R^2 модели KNN регрессии: {r2_knn}')

plt.scatter(y_test, y_pred_knn)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Реальные значения')
plt.ylabel('Предсказанные значения')
plt.title('Визуализация регрессии (KNN регрессия)')
plt.show()

"""####Многослойный перцептрон"""

from sklearn.neural_network import MLPRegressor

mlp_model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=42)

mlp_model.fit(X_train, y_train)

y_pred_mlp = mlp_model.predict(X_test)

r2_mlp = r2_score(y_test, y_pred_mlp)
print(f'Оценка R^2 модели MLP: {r2_mlp}')

plt.scatter(y_test, y_pred_mlp)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Реальные значения')
plt.ylabel('Предсказанные значения')
plt.title('Визуализация регрессии (MLP)')
plt.show()

"""####Дерево решений"""

from sklearn.tree import DecisionTreeRegressor

tree_model = DecisionTreeRegressor(random_state=42)

tree_model.fit(X_train, y_train)

y_pred_tree = tree_model.predict(X_test)

r2_tree = r2_score(y_test, y_pred_tree)
print(f'Оценка R^2 модели дерева решений: {r2_tree}')

plt.scatter(y_test, y_pred_tree)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Реальные значения')
plt.ylabel('Предсказанные значения')
plt.title('Визуализация регрессии (Дерево решений)')
plt.show()

"""####Другие методы

a. Гребневая регрессия
"""

from sklearn.linear_model import Ridge

ridge_model = Ridge(alpha=1.0)

ridge_model.fit(X_train, y_train)

y_pred_ridge = ridge_model.predict(X_test)

r2_ridge = r2_score(y_test, y_pred_ridge)
print(f'Оценка R^2 модели гребневой регрессии: {r2_ridge}')

plt.scatter(y_test, y_pred_ridge)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Реальные значения')
plt.ylabel('Предсказанные значения')
plt.title('Визуализация регрессии (Гребневая регрессия)')
plt.show()

"""b. Регрессия Лассо"""

from sklearn.linear_model import Lasso

lasso_model = Lasso(alpha=1.0)


lasso_model.fit(X_train, y_train)

y_pred_lasso = lasso_model.predict(X_test)

r2_lasso = r2_score(y_test, y_pred_lasso)
print(f'Оценка R^2 модели регрессии Лассо: {r2_lasso}')

plt.scatter(y_test, y_pred_lasso)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Реальные значения')
plt.ylabel('Предсказанные значения')
plt.title('Визуализация регрессии (Регрессия Лассо)')
plt.show()

"""c. Регрессия ElasticNet"""

from sklearn.linear_model import ElasticNet

elasticnet_model = ElasticNet(alpha=1.0, l1_ratio=0.5)  # Укажите значения alpha и l1_ratio по вашему выбору

elasticnet_model.fit(X_train, y_train)

y_pred_elasticnet = elasticnet_model.predict(X_test)

r2_elasticnet = r2_score(y_test, y_pred_elasticnet)
print(f'Оценка R^2 модели регрессии ElasticNet: {r2_elasticnet}')

plt.scatter(y_test, y_pred_elasticnet)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Реальные значения')
plt.ylabel('Предсказанные значения')
plt.title('Визуализация регрессии (ElasticNet)')
plt.show()

"""d. Случайный лес"""

from sklearn.ensemble import RandomForestRegressor

random_forest_model = RandomForestRegressor(n_estimators=100, random_state=42)  # Укажите количество деревьев (n_estimators) по вашему выбору

random_forest_model.fit(X_train, y_train)

y_pred_random_forest = random_forest_model.predict(X_test)

r2_random_forest = r2_score(y_test, y_pred_random_forest)
print(f'Оценка R^2 модели случайного леса: {r2_random_forest}')

plt.scatter(y_test, y_pred_random_forest)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Реальные значения')
plt.ylabel('Предсказанные значения')
plt.title('Визуализация регрессии (Случайный лес)')
plt.show()

"""e. Беггинг"""

from sklearn.ensemble import BaggingRegressor

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

base_model = LinearRegression()

bagging_model = BaggingRegressor(base_model, n_estimators=100, random_state=42)  # Укажите количество базовых моделей (n_estimators) по вашему выбору

bagging_model.fit(X_train, y_train)

y_pred_bagging = bagging_model.predict(X_test)

r2_bagging = r2_score(y_test, y_pred_bagging)
print(f'Оценка R^2 модели с беггингом: {r2_bagging}')

plt.scatter(y_test, y_pred_bagging)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Реальные значения')
plt.ylabel('Предсказанные значения')
plt.title('Визуализация регрессии (Беггинг)')
plt.show()

"""###Задание №3"""

from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

def train_and_evaluate_models(X, y):

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(),
        "Lasso Regression": Lasso(),
        "ElasticNet Regression": ElasticNet(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        "Bagging": BaggingRegressor(base_estimator=LinearRegression(), n_estimators=100, random_state=42),
        "Support Vector Machine": SVR(kernel='linear')
    }

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        print(f'{name}: Оценка R^2 - {r2:.4f}')

        plt.scatter(y_test, y_pred)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
        plt.xlabel('Реальные значения')
        plt.ylabel('Предсказанные значения')
        plt.title(f'Визуализация регрессии ({name})')
        plt.show()

train_and_evaluate_models(X, y)

"""###Задание №4"""

import matplotlib.pyplot as plt
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

diabetes = load_diabetes(as_frame=True)
X_diabetes = diabetes.data
y_diabetes = diabetes.target

print(X_diabetes.head())
print(X_diabetes.info())

#train_and_evaluate_models(X_diabetes, y_diabetes)