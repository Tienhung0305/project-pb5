import time
from datetime import datetime
import cloudinary.uploader

import paho.mqtt.client as mqtt
import requests
import json

from webcamFindPlate import findPlate, find_plate_inf
import cv2
import urllib.request
import numpy as np

# faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#mở video 
# video_capture = cv2.VideoCapture(0)

urlcam = "http://192.168.1.9/cam-lo.jpg"
broker_address = "192.168.1.2"

cloudinary.config(
  cloud_name = "damlykdtx",
  api_key = "386381942394164",
  api_secret = "mEvNmbgAMYivaAwhtpybdjsvGgk"
)
out = ""
# cv2.namedWindow("gotcha", cv2.WINDOW_AUTOSIZE)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("rs-in")

def on_message(client, userdata, msg):
    
    print(msg.payload)
    src = msg.payload.decode('utf-8')
    print(src)

client = mqtt.Client()
client.connect(broker_address)
client.on_message = on_message
# client.connect("192.168.137.1", 8900, 60)
oldPlate = 0
while True:
    # Capture frame-by-frame
    # ret, frame = video_capture.read()# cắt ảnh từ video liên tục

    imgResponse = urllib.request.urlopen(urlcam)
    imgnP = np.array(bytearray(imgResponse.read()), dtype = np.uint8)
    frame = cv2.imdecode(imgnP, -1)

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    x, y, w, h = findPlate(frame)
    
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow('Video', frame)
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
    if len(plate_info) >= 7:
        response = requests.request("GET",url,headers =  headers,data = payload)


    # if plate_info == "90B299999":
    #     client.publish("resultPlate", "1")
    
        if(response.status_code == 200 ):
            print("code response: ",response.status_code)
            print("plate: ",plate_info)
            client.publish("rs-in", "i")
            
            # lưu hình ảnh 
            if oldPlate != plate_info:
                
                # image = "10.jpg" # Đường dẫn tới ảnh cần upload
                
                now = datetime.now()
                timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                # Các thông tin cần post lên API
                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                
                public_id  = dt_string.replace("-","").replace(":","").replace(" ","") # Public ID mà bạn muốn chỉ định cho ảnh
                print(public_id)
                
                # result = cloudinary.uploader.upload(imgData, public_id=dt_string)
                
                name = "historyImage_out.jpg"
                cv2.imwrite(name,frame)
                upload_result = cloudinary.uploader.upload(name, public_id=public_id, filename=public_id)
                image_url = upload_result['secure_url']
                url = "http://localhost:1994/api/History/Post"
                print(dt_string)
                data = {
                    "id_history": public_id,
                    "isout": True,
                    "time": timestamp,
                    "image": image_url,
                    "number_plate": "90B299999"
                }
                headers = {"Content-Type": "application/json"}
                response = requests.post(url, data=json.dumps(data), headers=headers)
                if(response.status_code == 200):
                    print("POST: OK")
                else:
                    print("POST: FAILED")
            oldPlate = plate_info

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.1)
cv2.destroyAllWindows()
