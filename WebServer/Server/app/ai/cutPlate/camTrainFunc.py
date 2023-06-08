import serial
from PIL import Image
from urllib.request import urlopen
import cv2
import numpy as np
import pickle


# Sap xep contour tu trai sang phai
def sort_contours(cnts):

    reverse = False
    i = 0
    try:
        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
        return cnts
    except:
        return cnts

# Dinh nghia cac ky tu tren bien so
char_list =  '0123456789ABCDEFGHKLMNPRSTUVXYZ'

# Ham fine tune bien so, loai bo cac ki tu khong hop ly
def adjust_result(lp):
    result = ""
    for i in range(len(lp)):
        if lp[i] in char_list:
            result += lp[i]
    return result

def find_plate_inf(binary, image, i):
    digit_w = 30
    digit_h = 60
    roi = image
    # Segment kí tự
    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thre_mor = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel3)# xu ly hinh thai hoc bo nhieu, cv2.MORPH_DILATE: gian chu ra
    #Phép toán giãn nở và phép co, de gian chữ số ra dễ tìm conture hơn
    cont, _  = cv2.findContours(thre_mor, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    plate_info = ""
##    i = 1;
    for c in sort_contours(cont):    
        (x, y, w, h) = cv2.boundingRect(c)    
        ratio = h/w
        approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
        if 1.5<=ratio<=4.5: # Chon cac contour dam bao ve ratio w/h
            if h/roi.shape[0]>=0.6: # Chon cac contour cao tu 60% bien so tro len
                
                # Ve khung chu nhat quanh so
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
                #cv2.drawContours(roi, c,  -1, (0, 255, 0), 2)
                ##cv2.imshow(str(i),number)
                

                # Tach so va predict
                curr_num = thre_mor[y:y+h,x:x+w]# tach so
                curr_num = cv2.resize(curr_num, dsize=(digit_w, digit_h))
                _,curr_num = cv2.threshold(curr_num, 30, 255, cv2.THRESH_BINARY)
                #luu anh
                name = str(i)+".jpg"
                i = i+1;
                cv2.imwrite(name, curr_num)
                curr_num = np.array(curr_num,dtype=np.float32)
                curr_num = curr_num.reshape(-1, digit_w * digit_h)# chuyen mang 2 chieu ve mang 1 chieu
                
                # Dua vao model SVM
                fileName = 'train.xml'
                model_svm = pickle.load(open(fileName, 'rb'))

                result = model_svm.predict(curr_num)[0]

                if result<=9: # Neu la so thi hien thi luon
                    result = str(result)
                else: #Neu la chu thi chuyen bang ASCII
                    result = chr(result)

                plate_info +=result

    return  plate_info


def findPlate(Ivehicle):
    gray = cv2.cvtColor(Ivehicle, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    contours,h1 = cv2.findContours(thresh,1,cv2.CHAIN_APPROX_SIMPLE)

    #largest_rectangle = [0,0]#luu dien tich, contour co dt lon nhat
    largest_rectangle = [cv2.contourArea(contours[0]),contours[0]]
    imageCopy = Ivehicle.copy()
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        if len(approx)==4:
            x1,y1,w1,h1 = cv2.boundingRect(cnt)# lay toan do cua bien so
            image=imageCopy[y1:y1+h1,x1:x1+w1]
            cv2.rectangle(imageCopy, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
            #cv2.drawContours(imageCopy, largest_rectangle[1],  -1, (0, 255, 0), 2)
            
            area = cv2.contourArea(cnt)
            x,y,w,h = cv2.boundingRect(cnt)
            if area > largest_rectangle[0]:
                if (3.4<=w/h<=5.2)or(1.2<=w/h<=1.6):
                    largest_rectangle = [cv2.contourArea(cnt), cnt]
                    
    x1,y1,w1,h1 = cv2.boundingRect(largest_rectangle[1])# lay toan do cua bien so

    ##cv2.waitKey()(w1)
    ##cv2.waitKey()(h1)
    image=Ivehicle[y1:y1+h1,x1:x1+w1]
    return x1,y1,w1,h1


 
