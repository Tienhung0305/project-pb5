import cv2

import os
import numpy as np
import glob
import matplotlib.pyplot as plt
from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split
import pickle

digit_w = 30
digit_h = 60

def get_digit_data(path):#:,d igit_list, label_list):

    digit_list = []
    label_list = []

    for number in range(10):
        i=0
        for img_org_path in glob.iglob(path + str(number) + '/*.jpg'):
            print(img_org_path)
            img = cv2.imread(img_org_path, 0)
            img = np.array(img)
            img = img.reshape(-1, digit_h * digit_w) # chuyển về mảng 1 chiều
 
            print(img.shape)

            digit_list.append(img) # thêm mt img vào digit_list
            label_list.append([int(number)]) # thêm tên kí tự cân train

    for number in range(65, 91):
        #number = chr(number)
        print(number)
        i=0
        for img_org_path in glob.iglob(path + str(number) + '/*.jpg'):
            print(img_org_path)
            img = cv2.imread(img_org_path, 0)
            img = np.array(img)
            img = img.reshape(-1, digit_h * digit_w)
            print(img.shape)

            digit_list.append(img)
            label_list.append([int(number)])

    return  digit_list, label_list

#lấy dữ liệu
digit_path = "data/"
digit_list, label_list = get_digit_data(digit_path)

digit_list = np.array(digit_list, dtype=np.float32)

digit_list = digit_list.reshape(-1, digit_h * digit_w)

label_list = np.array(label_list)
label_list = label_list.reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(digit_list, label_list, test_size = 0.2, shuffle = True)
classifier = svm.SVC()
classifier.fit(X_train, y_train)

fileName = "train.xml"
pickle.dump(classifier, open(fileName, "wb"))

loaded_model = pickle.load(open(fileName, 'rb'))
print(digit_list[1])
result = loaded_model.predict([X_test[10]])
print("==")
print(result)


predicted = classifier.predict(X_test)
print(metrics.classification_report(y_test, predicted))
# metrics.plot_confusion_matrix(classifier, X_test, y_test)
plt.show()
