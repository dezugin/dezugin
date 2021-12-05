import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn import svm
from sklearn.model_selection import cross_validate
from sklearn.metrics import recall_score
X, y = datasets.load_iris(return_X_y=True)
X.shape, y.shape
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, random_state=0)

X_train.shape, y_train.shape

X_test.shape, y_test.shape

clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
clf.score(X_test, y_test)

scoring = ['precision_macro', 'recall_macro','f1_macro']
clf = svm.SVC(kernel='linear', C=1, random_state=0)
accuracy = cross_val_score(clf, X, y, cv=5)
precision = cross_validate(clf, X, y, scoring=scoring[0])
precision = precision['test_score']
recall = cross_validate(clf, X, y, scoring=scoring[1])
recall = recall['test_score']
f1 = cross_validate(clf, X, y, scoring=scoring[2])
f1 = f1['test_score']
print("%0.5f accuracy with a standard deviation of %0.2f" % (accuracy.mean(), accuracy.std()))
print("%0.5f precision with a standard deviation of %0.2f" % (precision.mean(), precision.std()))
print("%0.5f recall with a standard deviation of %0.2f" % (recall.mean(), recall.std()))
print("%0.5f f1 with a standard deviation of %0.2f" % (f1.mean(), f1.std()))
