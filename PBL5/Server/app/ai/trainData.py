

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
            img = cv2.imread(img_org_path, 0)
            img = np.array(img)
            img = img.reshape(-1, digit_h * digit_w) # chuyển về mảng 1 chiều
            digit_list.append(img) # thêm mt img vào digit_list
            label_list.append([int(number)]) # thêm tên kí tự cân train
    for number in range(65, 91):
        i=0
        for img_org_path in glob.iglob(path + str(number) + '/*.jpg'):
            img = cv2.imread(img_org_path, 0)
            img = np.array(img)
            img = img.reshape(-1, digit_h * digit_w)
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

y_train = np.ravel(y_train)
y_test = np.ravel(y_test)

classifier = svm.SVC()
classifier.fit(X_train, y_train)

fileName = "train.xml"
pickle.dump(classifier, open(fileName, "wb"))
loaded_model = pickle.load(open(fileName, 'rb'))
predicted = classifier.predict(X_test)
print(metrics.classification_report(y_test, predicted))


# # Test performance
# test_image_file = "2.jpg"
# test_image = cv2.imread(test_image_file)

# # Preprocess the test image
# test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
# test_image = cv2.resize(test_image, (digit_w, digit_h))
# test_image = np.array(test_image)
# test_image = test_image.reshape(1, digit_h * digit_w).astype(np.float32)

# # Predict the label of the test image
# predicted_label = loaded_model.predict(test_image)

# # Print the predicted label
# print("Predicted label:", predicted_label)


