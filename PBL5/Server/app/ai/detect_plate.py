import requests
from webcamFindPlate import findPlate, find_plate_inf
import cv2
import urllib.request as urlrequest
import numpy as np

def plate_detect(urlIMG):

    urlcam = "linkanh"

    isValidPlate = False

    # Capture frame-by-frame
    # cắt ảnh từ video liên tục

    imgResponse = urlrequest.urlopen(urlcam)
    imgnP = np.array(bytearray(imgResponse.read()), dtype = np.uint8)
    frame = cv2.imdecode(imgnP, -1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    x, y, w, h = findPlate(frame)

    #lấy ảnh biển số
    image=frame[y:y+h,x:x+w]
    if w/h > 2:
        image = cv2.resize(image, (470, 110))# 0:h
        
    else:
        image = cv2.resize(image, (315, 235))
    
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (3,3), 0) # lam mo de giam gay nhieu
    # Ap dung threshold de phan tach so va nen
    binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] #tách ngưỡng

    if w/h > 2:
        plate_info = find_plate_inf(binary, image, 1)
    else:
    
        h = int(image.shape[0]/2) #cắt đôi biển số xe máy          
        p1 = binary[0:h,0:image.shape[1]]
        p2 = binary[h:image.shape[0],0:image.shape[1]]
        image_p1 = image[0:h,0:image.shape[1]]
        image_p2 = image[h:image.shape[0],0:image.shape[1]]

        plate_info = find_plate_inf(p1, image_p1, 1)
        plate_info = plate_info + find_plate_inf(p2, image_p2, 5)


    # print("code response: ",response.status_code)
    print("\nplate <8: ",plate_info)
    url = "http://localhost:1994/api/Vehicle/CheckInvalid?number_plate="+plate_info 
    payload = {}
    headers = {}
    response = requests.request("GET",url,headers =  headers,data = payload)

    if(response.status_code == 200 ):
        isValidPlate
        
    return isValidPlate
