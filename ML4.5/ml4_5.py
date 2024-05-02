# -*- coding: utf-8 -*-
"""ML4_5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pquMTLsWVqs04lv_EcYqQ5iI-H8BBLWT

##Методические указания
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import make_classification
X, Y = make_classification(n_samples=1000, n_classes=2, n_features=5, n_redundant=0, random_state=1)

X.shape, Y.shape

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

X_train.shape, Y_train.shape

X_test.shape, Y_test.shape

import pandas as pd

from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.linear_model import SGDClassifier

names = ["Nearest_Neighbors", "Linear_SVM", "Polynomial_SVM", "RBF_SVM", "Gaussian_Process",
         "Gradient_Boosting", "Decision_Tree", "Extra_Trees", "Random_Forest", "Neural_Net", "AdaBoost",
         "Naive_Bayes", "QDA", "SGD"]

classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    SVC(kernel="poly", degree=3, C=0.025),
    SVC(kernel="rbf", C=1, gamma=2),
    GaussianProcessClassifier(1.0 * RBF(1.0)),
    GradientBoostingClassifier(n_estimators=100, learning_rate=1.0),
    DecisionTreeClassifier(max_depth=5),
    ExtraTreesClassifier(n_estimators=10, min_samples_split=2),
    RandomForestClassifier(max_depth=5, n_estimators=100),
    MLPClassifier(alpha=1, max_iter=1000),
    AdaBoostClassifier(n_estimators=100),
    GaussianNB(),
    QuadraticDiscriminantAnalysis(),
    SGDClassifier(loss="hinge", penalty="l2")]

scores = []
for name, clf in zip(names, classifiers):
    clf.fit(X_train, Y_train)
    score = clf.score(X_test, Y_test)
    scores.append(score)

import pandas as pd
import seaborn as sns

df = pd.DataFrame()
df['name'] = names
df['score'] = scores
df.sort_values(by=["score"], ascending=False, inplace=True)
df

cm = sns.light_palette("green", as_cmap=True)
s = df.style.background_gradient(cmap=cm)
s

sns.set(style="whitegrid")
ax = sns.barplot(y="name", x="score", data=df)

df = pd.read_csv("Advertising.csv")

df.head()

## Создаём X и y
X = df.drop('sales',axis=1)
y = df['sales']

# Разбиение на обучающий и тестовый наборы - TRAIN TEST SPLIT
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

# Масштабирование данных (SCALE)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

from sklearn.linear_model import ElasticNet

help(ElasticNet)

base_elastic_model = ElasticNet()

param_grid = {'alpha':[0.1,1,5,10,50,100],
              'l1_ratio':[.1, .5, .7, .9, .95, .99, 1]}

from sklearn.model_selection import GridSearchCV

# число verbose выбирайте сами
grid_model = GridSearchCV(estimator=base_elastic_model,
                          param_grid=param_grid,
                          scoring='neg_mean_squared_error',
                          cv=5,
                          verbose=2)

grid_model.fit(X_train,y_train)

grid_model.best_estimator_

y_pred = grid_model.predict(X_test)

from sklearn.metrics import mean_squared_error
mean_squared_error(y_test,y_pred)

"""##Контрольные вопросы

#### 1. Зачем нужно производить оптимизацию гиперпараметров?

Оптимизация гиперпараметров необходима для улучшения производительности модели на новых данных. Гиперпараметры — это параметры, которые задаются до начала обучения модели и не изменяются в процессе обучения. Правильная настройка этих параметров позволяет достичь лучшей точности, стабильности и эффективности модели.

#### 2. В чём заключается процесс оптимизации гиперпараметров?

1.   Определение гиперпараметров для оптимизации.
2.   Выбор стратегии поиска (например, полный перебор, случайный поиск, байесовская оптимизация).
3. Выбор метрики оценки модели, которая будет использоваться для сравнения разных наборов гиперпараметров.
4. Использование кросс-валидации для оценки модели на разных подвыборках данных.
5. Анализ результатов и выбор наилучших гиперпараметров.

####3. В чем достоинства и недостатки метода gridsearchcv?

**Достоинства:**

* Простота использования и понимания: метод легко реализовать и интерпретировать.

* Исчерпывающий поиск: проверяет каждую комбинацию гиперпараметров, что гарантирует нахождение наилучшего решения в рамках заданного пространства параметров.

* Автоматическая кросс-валидация: обеспечивает надежную оценку производительности модели.

**Недостатки:**

* Высокая вычислительная стоимость: требует большого количества времени и ресурсов, особенно при большом количестве гиперпараметров и их возможных значений.

* Ограниченность поискового пространства: поиск ограничивается заранее определенной сеткой значений, и лучший набор параметров может находиться между проверенными точками.

* Масштабируемость: с увеличением количества параметров экспоненциально растет количество комбинаций, что делает GridSearchCV менее эффективным для больших наборов данных.

####4. Какие еще стратегии оптимизации гиперпараметров существуют?

* Random Search: случайный выбор значений гиперпараметров из заданного пространства, что часто более эффективно, чем полный перебор, особенно в случаях с большим числом параметров.

* Bayesian Optimization: использует статистическую модель для предсказания областей поиска, где гиперпараметры могут улучшить производительность модели, что обычно более эффективно, чем случайный поиск.

* Genetic Algorithms: применяют подходы, основанные на идеях эволюции и естественного отбора, для определения наилучших гиперпараметров.

* Gradient-based optimization: подходы, использующие градиенты для оптимизации гиперпараметров, применимы в некоторых типах моделей.

####5. Почему при использовании GridSearchCV не нужна валидационная выборка?

GridSearchCV автоматически использует кросс-валидацию для оценки каждой комбинации гиперпараметров, обеспечивая объективное сравнение их эффективности. Это позволяет оценить модель на разных подвыборках обучающего набора данных, исключая необходимость отдельной валидационной выборки. Каждый раздел данных используется и как часть обучающего набора, и как часть валидационного, что обеспечивает эффективное и полное использование доступных данных для оценки модели.
"""