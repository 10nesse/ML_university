# -*- coding: utf-8 -*-
"""ML2_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fmCULx19mHaJ3nif6W_NzW_l1j5vbcqk

##Методические указания
"""

import pandas as pd

data = pd.read_csv("https://raw.githubusercontent.com/koroteevmv/ML_course/2023/ML2.2%20real%20classification/data/diabetes.csv")

data.head()

data.info()

data.describe()

y = data.Outcome
X = data.drop(["Outcome"], axis=1)

y.shape, X.shape

from sklearn.linear_model import LogisticRegression
logistic = LogisticRegression()
logistic.fit(X, y)

print("Coefficients: \n", logistic.coef_[0])

_ = [print(k, v) for k, v in zip(X.columns, logistic.coef_[0])]

print("Intercept: \n", logistic.intercept_)

y_pred = logistic.predict(X)

_ = [print(a, b) for a, b in list(zip(y, y_pred))[:10]]

from sklearn import metrics
metrics.confusion_matrix(y, y_pred)

import seaborn as sns
sns.heatmap(metrics.confusion_matrix(y, y_pred), annot=True)

logistic.score(X, y)

metrics.accuracy_score(y_test, y_pred)

from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(2)

poly = poly.fit_transform(X)
poly

polynomial = LogisticRegression()
polynomial.fit(poly, y)
y_pred_poly = polynomial.predict(poly)

"""##Задания для самостоятельного выполнения

#### 1. Изучите документацию sklearn, посвященную классу LogisticRegression. Какую еще информацию можно вывести для обученной модели? Попробуйте изменить аргументы при создании модели и посмотрите, как это влияет на качество предсказания.
"""

# Расчет точности
accuracy = logistic.score(X, y)
print("Accuracy: ", accuracy)

# Вывод вероятностей для каждого класса
probabilities = logistic.predict_proba(X)
print("Predicted Probabilities:\n", probabilities)

# Значения решающей функции
decision_values = logistic.decision_function(X)
print("Decision Function Values:\n", decision_values)

# Получение параметров модели
params = logistic.get_params()
print("Model Parameters:\n", params)

# Выделение целевой переменной и факторов
y = data.Outcome
X = data.drop(["Outcome"], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание и обучение модели с базовыми параметрами
logistic_base = LogisticRegression()
logistic_base.fit(X_train, y_train)

# Оценка базовой модели
print("Base Model Accuracy:", logistic_base.score(X_test, y_test))

# Создание и обучение модели с измененными параметрами
logistic_tuned = LogisticRegression(penalty='l1', C=1000, solver='liblinear', max_iter=1000, class_weight='balanced', random_state=42)
logistic_tuned.fit(X_train, y_train)

# Оценка модели с измененными параметрами
print("Tuned Model Accuracy:", logistic_tuned.score(X_test, y_test))

"""#### 2.Попробуйте применить к той же задаче другие модели классификации. Для каждой из них выведите матрицу классификации и оценку точности. Рекомендуется исследовать следующие модели:

##### i. Метод опорных векторов
"""

from sklearn.svm import SVC
import matplotlib.pyplot as plt

# Разделение на обучающий и тестовый наборы данных
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Метод опорных векторов (SVM) без ядра
svm_no_kernel = SVC(kernel='linear', random_state=42)
svm_no_kernel.fit(X_train, y_train)

# Визуализация матрицы классификации для SVM (No Kernel)
sns.heatmap(metrics.confusion_matrix(y_test, svm_no_kernel.predict(X_test)), annot=True,  fmt='d', cmap='Blues', xticklabels=['0', '1'], yticklabels=['0', '1'])
plt.title('Confusion Matrix - SVM (No Kernel)')
plt.show()

# Метод опорных векторов (SVM) с линейным ядром
svm_linear = SVC(kernel='linear', random_state=42)
svm_linear.fit(X_train, y_train)

# Визуализация матрицы классификации для SVM (Linear Kernel)
sns.heatmap(metrics.confusion_matrix(y_test, svm_linear.predict(X_test)), annot=True,  fmt='d', cmap='Blues', xticklabels=['0', '1'], yticklabels=['0', '1'])
plt.title('Confusion Matrix - SVM (Linear Kernel)')
plt.show()

# Метод опорных векторов (SVM) с полиномиальным ядром
svm_poly = SVC(kernel='poly', degree=3, random_state=42)
svm_poly.fit(X_train, y_train)

# Визуализация матрицы классификации для SVM (Polynomial Kernel)
sns.heatmap(metrics.confusion_matrix(y_test, svm_poly.predict(X_test)), annot=True,  fmt='d', cmap='Blues', xticklabels=['0', '1'], yticklabels=['0', '1'])
plt.title('Confusion Matrix - SVM (Polynomial Kernel)')
plt.show()

# Метод опорных векторов (SVM) с гауссовым ядром
svm_rbf = SVC(kernel='rbf', random_state=42)
svm_rbf.fit(X_train, y_train)

# Визуализация матрицы классификации для SVM (RBF Kernel)
sns.heatmap(metrics.confusion_matrix(y_test, svm_rbf.predict(X_test)), annot=True,  fmt='d', cmap='Blues', xticklabels=['0', '1'], yticklabels=['0', '1'])
plt.title('Confusion Matrix - SVM (RBF Kernel)')
plt.show()

"""##### ii. Метод ближайших соседей"""

from sklearn.neighbors import KNeighborsClassifier

# Метод ближайших соседей (KNN)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# Оценка модели KNN
print("KNN Accuracy:", knn.score(X_test, y_test))

# Визуализация матрицы классификации для KNN
sns.heatmap(metrics.confusion_matrix(y_test, knn.predict(X_test)), annot=True,  fmt='d', cmap='Blues', xticklabels=['0', '1'], yticklabels=['0', '1'])
plt.title('Confusion Matrix - KNN')
plt.show()

"""##### iii. Многослойный перцептрон

"""

from sklearn.neural_network import MLPClassifier

# Многослойный перцептрон (MLP)
mlp = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)
mlp.fit(X_train, y_train)

# Оценка модели MLP
print("MLP Accuracy:", mlp.score(X_test, y_test))

# Визуализация матрицы классификации для MLP
sns.heatmap(metrics.confusion_matrix(y_test, mlp.predict(X_test)), annot=True,  fmt='d', cmap='Blues', xticklabels=['0', '1'], yticklabels=['0', '1'])
plt.title('Confusion Matrix - MLP')
plt.show()

"""##### iv. Дерево решений

"""

from sklearn.tree import DecisionTreeClassifier

# Дерево решений
decision_tree = DecisionTreeClassifier(random_state=42)
decision_tree.fit(X_train, y_train)

# Оценка модели Дерева решений
print("Decision Tree Accuracy:", decision_tree.score(X_test, y_test))

# Визуализация матрицы классификации для Дерева решений
sns.heatmap(metrics.confusion_matrix(y_test, decision_tree.predict(X_test)), annot=True,  fmt='d', cmap='Blues', xticklabels=['0', '1'], yticklabels=['0', '1'])
plt.title('Confusion Matrix - Decision Tree')
plt.show()

"""##### v. Наивный байесовский классификатор"""

from sklearn.naive_bayes import GaussianNB

# Наивный байесовский классификатор (Gaussian Naive Bayes)
naive_bayes = GaussianNB()
naive_bayes.fit(X_train, y_train)

# Оценка модели Наивного байесовского классификатора
print("Naive Bayes Accuracy:", naive_bayes.score(X_test, y_test))

# Визуализация матрицы классификации для Наивного байесовского классификатора
sns.heatmap(metrics.confusion_matrix(y_test, naive_bayes.predict(X_test)), annot=True,  fmt='d', cmap='Blues', xticklabels=['0', '1'], yticklabels=['0', '1'])
plt.title('Confusion Matrix - Naive Bayes')
plt.show()

"""##### vi. (*) Другие методы:

###### a. Пассивно-агрессивный классификатор
"""

from sklearn.linear_model import PassiveAggressiveClassifier

# Пассивно-агрессивный классификатор
pac_classifier = PassiveAggressiveClassifier(max_iter=1000)
pac_classifier.fit(X_train, y_train)

# Визуализация матрицы классификации для Пассивно-агрессивного классификатора
sns.heatmap(metrics.confusion_matrix(y_test, pac_classifier.predict(X_test)), annot=True,  fmt='d', cmap='Blues', xticklabels=['0', '1'], yticklabels=['0', '1'])
plt.title("Confusion Matrix - Passive Aggressive Classifier")
plt.show()

"""###### b. Гребневый классификатор"""

from sklearn.linear_model import RidgeClassifierCV

# Гребневый классификатор с автоматическим подбором параметра регуляризации (alpha)
ridge_classifier = RidgeClassifierCV(alphas=[1e-3, 1e-2, 1e-1, 1])
ridge_classifier.fit(X_train, y_train)

# Визуализация матрицы классификации для Гребневого классификатора
sns.heatmap(metrics.confusion_matrix(y_test, ridge_classifier.predict(X_test)), annot=True,  fmt='d', cmap='Blues', xticklabels=['0', '1'], yticklabels=['0', '1'])
plt.title("Confusion Matrix - Ridge Classifier")
plt.show()

"""###### c. Случайный лес"""

from sklearn.ensemble import RandomForestClassifier

# Модель случайного леса
random_forest = RandomForestClassifier(n_estimators=100, random_state=42)
random_forest.fit(X_train, y_train)

# Оценка модели случайного леса
print("Random Forest Accuracy:", random_forest.score(X_test, y_test))

# Визуализация матрицы классификации для случайного леса
sns.heatmap(metrics.confusion_matrix(y_test, random_forest.predict(X_test)), annot=True,  fmt='d', cmap='Blues', xticklabels=['0', '1'], yticklabels=['0', '1'])
plt.title("Confusion Matrix - Random Forest")
plt.show()

"""###### d. Беггинг"""

from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

# Беггинг с деревьями решений
base_classifier = DecisionTreeClassifier(random_state=42)
bagging_classifier = BaggingClassifier(base_classifier, n_estimators=100, random_state=42)
bagging_classifier.fit(X_train, y_train)

# Оценка модели беггинга
print("Bagging Accuracy:", bagging_classifier.score(X_test, y_test))

# Визуализация матрицы классификации для беггинга
sns.heatmap(metrics.confusion_matrix(y_test, bagging_classifier.predict(X_test)), annot=True,  fmt='d', cmap='Blues', xticklabels=['0', '1'], yticklabels=['0', '1'])
plt.title("Confusion Matrix - Bagging")
plt.show()

"""#### 3.Напишите функцию, которая автоматически обучает все перечисленные модели и для каждой выдает оценку точности."""

def train_and_evaluate_models(X_train, y_train, X_test, y_test):
    models = {
        'Logistic Regression': LogisticRegression(),
        'Support Vector Machine (Linear Kernel)': SVC(kernel='linear'),
        'Support Vector Machine (RBF Kernel)': SVC(kernel='rbf'),
        'Support Vector Machine (Polynomial Kernel)': SVC(kernel='poly', degree=3),
        'Support Vector Machine (Sigmoid Kernel)': SVC(kernel='sigmoid'),
        'K-Nearest Neighbors': KNeighborsClassifier(),
        'Multi-layer Perceptron': MLPClassifier(max_iter=1000),
        'Decision Tree': DecisionTreeClassifier(),
        'Naive Bayes': GaussianNB(),
        'Passive-Aggressive Classifier': PassiveAggressiveClassifier(max_iter=1000),
        'Ridge Classifier': RidgeClassifierCV(),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Bagging': BaggingClassifier(DecisionTreeClassifier(random_state=42), n_estimators=100, random_state=42)
    }

    for model_name, model in models.items():
        model.fit(X_train, y_train)
        accuracy = model.score(X_test, y_test)
        print(f"{model_name} Accuracy: {accuracy:.4f}")


# Обучение и оценка моделей
train_and_evaluate_models(X_train, y_train, X_test, y_test)

"""#### 4. Повторите полностью анализ для другой задачи - распознавание вида ириса по параметрам растения (можно использовать метод sklearn.datasets.load_iris())."""

from sklearn.datasets import load_iris

# Загрузка данных
iris = load_iris()
data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
data['Species'] = iris.target_names[iris.target]

# Выделение целевой переменной и факторов
y = iris.target
X = iris.data

# Разделение на обучающий и тестовый наборы данных
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=36)

# Обучение и оценка моделей
train_and_evaluate_models(X_train, y_train, X_test, y_test)