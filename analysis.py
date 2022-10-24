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

df = pd.read_csv('data.csv')
X = df.drop(['League Rank'], axis=1)
y_data = df['League Rank']

# plt.scatter(df['Points'].sample(100), y_data.sample(100))
# plt.xlabel('Wins')
# plt.ylabel('League Rank')
# plt.show()
sns.regplot(x='Wins', y='League Rank', data=df)

MinMaxScaler = preprocessing.MinMaxScaler()
X_data_minmax = MinMaxScaler.fit_transform(X)
data = pd.DataFrame(X_data_minmax)

X_train, X_test, y_train, y_test = train_test_split(data, y_data, test_size=0.20, random_state=42)
knn_clf = KNeighborsClassifier()
knn_clf.fit(X_train, y_train)
y_pred = knn_clf.predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

result=confusion_matrix(y_test,y_pred)
# print(f"Confusion Matrix: {result}")

result1 = classification_report(y_test, y_pred)
# print(f"Classification Report: {result1}")

result2 = accuracy_score(y_test, y_pred)
print(f"Accuracy: {result2}")

test_data = [97, 45, 0.59, 252, 266]
test = np.array(test_data)

print(knn_clf.predict(test.reshape(1, -1)))