# import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
# import pandas as pd
# from sklearn import datasets, metrics
# from sklearn.metrics import classification_report, confusion_matrix
# from sklearn.model_selection import train_test_split

# # Use a Decision Tree for the ML model 
# df = pd.read_csv(r'data.csv')

# X = df[['Points', 'Points Percentage', 'Goals Against', 'Goals For']] 
# y = df[['League Rank']]

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 42)

# from sklearn.tree import DecisionTreeClassifier
# classifier = DecisionTreeClassifier(criterion='entropy', max_depth = 3, random_state=42)
# classifier.fit(X_train, y_train)
# y_pred_train = classifier.predict(X_train)

# from sklearn import metrics 
# from sklearn.metrics import confusion_matrix, classification_report
# accuracy = metrics.accuracy_score(y_train, y_pred_train)
# print("Accuracy: {:.2f}".format(accuracy))
# cm = confusion_matrix(y_train, y_pred_train)

# test_data = [116, 0.71, 202, 278]
# test = np.array(test_data)

# classifier.predict(test.reshape(-1, 4))
# # print('Confusion Matrix: \n', cm)
# # print(classification_report(y_train, y_pred_train))

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import pandas as pd 
import math
import data_augmentation
import data_preprocessing

df = pd.read_csv('regular_season_data.csv')

data_preprocessing.preprocessing(df)
print(len(df))
new_df = pd.DataFrame(data_augmentation.augmentation(df.values.tolist())).sample(frac = 1)

X = new_df.drop([5], axis=1)
X.columns = ['Points', 'Wins', 'Points Percentage', 'Goals For', 'Goals Against']

y = new_df[5]
y.columns = ['League Rank']

# Using KNN for the ML Model
MinMaxScaler = preprocessing.MinMaxScaler()
X_data_minmax = MinMaxScaler.fit_transform(X)
data = pd.DataFrame(X_data_minmax)

X_train, X_test, y_train, y_test = train_test_split(data, y, test_size=0.20, random_state=42)
knn_clf = KNeighborsClassifier()
mean_acc = np.zeros(20)
max = 0

# for i in range(1, 20):
#     knn_clf = KNeighborsClassifier(n_neighbors = i).fit(X_train, y_train)
#     y_pred = knn_clf.predict(X_test)
#     mean_acc[i - 1] = accuracy_score(y_test, y_pred)
    
from sklearn.model_selection import GridSearchCV
grid_params = { 'n_neighbors' : [1, 2, 3],
                'weights' : ['uniform', 'distance'],
                'metric' : ['minkowski', 'euclidean', 'manhattan']}
gs = GridSearchCV(KNeighborsClassifier(), grid_params, verbose=1, cv=3, n_jobs=-1)     

g_res = gs.fit(X_train, y_train)
g_res.best_score_
g_res.best_params_
knn_clf = KNeighborsClassifier(n_neighbors = 1, weights = 'uniform', algorithm = 'brute', metric = 'minkowski')
knn_clf.fit(X_train, y_train)
y_pred1 = knn_clf.predict(X_train)
y_pred2 = knn_clf.predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print('Training set accuracy: ', accuracy_score(y_train, y_pred1))
print('Test set accuracy: ', accuracy_score(y_test, y_pred2))

cm = confusion_matrix(y_test, y_pred2)
cr = classification_report(y_test, y_pred2)

from sklearn.model_selection import cross_val_score
scores = cross_val_score(knn_clf, X, y, cv=5)
print('Model accuracy: ', np.mean(scores))

test_data = [85, 37, 0.52, 230, 200]
test = np.array(test_data)

print(math.trunc(knn_clf.predict(test.reshape(1, -1)).tolist()[0]))

for column in X.columns:
    plt.scatter(X[column].sample(100), y.sample(100))
    plt.xlabel(str(column))
    plt.ylabel('League Rank')
    plt.show()
