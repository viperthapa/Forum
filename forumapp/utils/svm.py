#Import svm model
from sklearn import svm


def final_prediction(X_train,y_train):
    clf = svm.SVC(kernel='linear') # Linear Kernel
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    return y_pred