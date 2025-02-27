# -*- coding: utf-8 -*-
"""Plantilla Formulas.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_Gyq8gbbt5m7utVokuqSDQYgB8FytGr6
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.model_selection import train_test_split, KFold, RepeatedStratifiedKFold, GridSearchCV
from sklearn.metrics import classification_report, mean_squared_error, r2_score, log_loss
from sklearn.linear_model import ElasticNet, LogisticRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

# Commented out IPython magic to ensure Python compatibility.
!git clone https://github.com/it-ces/Analytics-puj.git
# %cd "Analytics-puj"
# %env OMP_NUM_THREADS = 4

url = "https://raw.githubusercontent.com/4GeeksAcademy/decision-tree-project-tutorial/main/diabetes.csv"
df = pd.read_csv(url)

y = df['Outcome']
X = df.drop('Outcome', axis=1).copy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

def grid_dt(X_train, y_train):
    model = DecisionTreeClassifier(random_state=42)
    class_weight =  [{0:0.5, 1:0.5}]
    criterion = ['gini', 'entropy', 'log_loss']
    max_depth = [2,3,5,7,10,20,30,40]
    min_samples_split = [2,5,10,20]
    min_samples_leaf = [1,2,5]
    max_leaf_nodes = [2,5,10,20]
    ccp_alpha = [0.001, 0.01, 0.1, 1, 10]
    splitter = ['best', 'random']
    grid = dict(criterion=criterion,
                class_weight= class_weight,
                max_depth = max_depth,
                min_samples_split = min_samples_split,
                min_samples_leaf = min_samples_leaf,
                splitter=splitter
                )
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=1, random_state=42)
    grid_search = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, cv=cv,
                           scoring='roc_auc',error_score='raise')
    grid_result = grid_search.fit(X_train, y_train)
    return  grid_result.best_estimator_

def grid_RandomForest(X_train, y_train):
  model = RandomForestClassifier(random_state=0)
  n_estimators = [100,250,500]
  criterion = ['gini', 'entropy', 'log_loss']
  min_samples_split = [0.05, 0.1,]
  max_depth = [2,3,4]
  grid = dict(n_estimators = n_estimators, criterion = criterion,
              min_samples_split = min_samples_split, max_depth = max_depth)
  cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=1, random_state=1)
  grid_search = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, cv=cv,
                            scoring='roc_auc',error_score='raise')
  grid_result = grid_search.fit(X_train, y_train)
  return  grid_result.best_estimator_

def grid_Adaboost(X_train, y_train):
    model = AdaBoostClassifier(random_state=1)
    n_estimators = [2, 15, 35, 50, 70, 100]
    learning_rate = np.linspace(0.01, 1, 10)
    grid = dict(n_estimators=n_estimators, learning_rate=learning_rate)
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=1, random_state=1)
    grid_search = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, cv=cv,
                               scoring='roc_auc', error_score='raise')
    grid_result = grid_search.fit(X_train, y_train)
    return grid_result.best_estimator_

best_rf = grid_RandomForest(X_train, y_train)
best_rf

best_dt = grid_dt(X_train, y_train)
best_dt

best_adaboost = grid_Adaboost(X_train, y_train)
best_adaboost

y_pred_rf = best_rf.predict(X_test)
print(classification_report(y_test, y_pred_rf))

y_pred_dt = best_dt.predict(X_test)
print(classification_report(y_test, y_pred_dt))

y_pred_ad = best_adaboost.predict(X_test)
print(classification_report(y_test, y_pred_ad))