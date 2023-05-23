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
video_capture = cv2.VideoCapture(0)

video_capture1 = cv2.VideoCapture(1)

mqtt_broker = "broker.emqx.io"
topic = "rs-out"
mqtt_username = "emqx"
mqtt_password = "public"
mqtt_port = 1883

cloudinary.config(
  cloud_name = "damlykdtx",
  api_key = "386381942394164",
  api_secret = "mEvNmbgAMYivaAwhtpybdjsvGgk"
)
out = ""
# cv2.namedWindow("gotcha", cv2.WINDOW_AUTOSIZE)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("rs-out")
    client.subscribe("rs-in")

def on_message(client, userdata, msg):
    # print(msg.payload)
    src = msg.payload.decode('utf-8')
    print(src)

# Create MQTT client instance
client = mqtt.Client()

# Set username and password
client.username_pw_set(mqtt_username, mqtt_password)

# Set up event callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(mqtt_broker, mqtt_port)
oldPlate_in = 0
oldPlate_out = 0
while True:
    # Capture frame-by-frame
    # ret, frame = video_capture.read()# cắt ảnh từ video liên tục

    ret1, frame_out = video_capture1.read()# cắt ảnh từ video liên tục
    ret1, frame_in = video_capture.read()# cắt ảnh từ video liên tục


    # imgResponse_in = urllib.request.urlopen(urlcam_in)
    # imgnP_in = np.array(bytearray(imgResponse_in.read()), dtype = np.uint8)
    # frame_in = cv2.imdecode(imgnP_in, -1)

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray_out = cv2.cvtColor(frame_out , cv2.COLOR_BGR2GRAY)

    # gray_in = cv2.cvtColor(frame_in, cv2.COLOR_BGR2GRAY)

    # imgResponse_out = urllib.request.urlopen(urlcam_out)
    # imgnP_out = np.array(bytearray(imgResponse_out.read()), dtype = np.uint8)
    # frame_out = cv2.imdecode(imgnP_out, -1)


    x_out, y_out, w_out, h_out = findPlate(frame_out)

    x_in, y_in, w_in, h_in = findPlate(frame_in)
    
    cv2.rectangle(frame_in, (x_in, y_in), (x_in + w_in, y_in + h_in), (0, 255, 0), 2)
    cv2.imshow('Video_IN', frame_in)

    cv2.rectangle(frame_out, (x_out, y_out), (x_out + w_out, y_out + h_out), (0, 255, 0), 2)
    cv2.imshow('Video_OUT', frame_out)


    #lấy ảnh biển số
    image_out = frame_out[y_out : y_out + h_out , x_out : x_out + w_out]

    image_in = frame_in[y_in : y_in + h_in, x_in : x_in +  w_in]

    if w_out / h_out > 2:
        image_out = cv2.resize(image_out , (470, 110))# 0:h
        
    else:
        image_out = cv2.resize(image_out , (315, 235))

    if w_in / h_in > 2:
        image_in = cv2.resize(image_in , (470, 110))# 0:h
        
    else:
        image_in = cv2.resize(image_in , (315, 235))
    
    
    gray_out = cv2.cvtColor(image_out , cv2.COLOR_BGR2GRAY)
    gray_in = cv2.cvtColor(image_in, cv2.COLOR_BGR2GRAY)
    blur_in = cv2.GaussianBlur(gray_in , (3,3), 0) # lam mo de giam gay nhieu
    # Ap dung threshold de phan tach so va nen
    binary_in = cv2.threshold(blur_in , 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] #tách ngưỡng

    blur_out = cv2.GaussianBlur(gray_out , (3,3), 0) # lam mo de giam gay nhieu
    # Ap dung threshold de phan tach so va nen
    binary_out = cv2.threshold(blur_out , 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] #tách ngưỡng

    if w_in / h_in > 2:
        plate_info_in = find_plate_inf(binary_in, image_in, 1)
    else:
    
        h_in = int(image_in.shape[0]/2) #cắt đôi biển số xe máy          
        p1_in = binary_in[0 : h_in , 0 : image_in.shape[1]]
        p2_in = binary_in[h_in : image_in.shape[0], 0 : image_in.shape[1]]
        image_p1_in = image_in[0 : h_in, 0 : image_in.shape[1]]
        image_p2_in = image_in[h_in : image_in.shape[0] , 0 : image_in.shape[1]]

        plate_info_in = find_plate_inf(p1_in, image_p1_in, 1)
        plate_info_in = plate_info_in + find_plate_inf(p2_in, image_p2_in, 5)




    if w_out / h_out > 2:
        plate_info_out = find_plate_inf(binary_out, image_out, 1)
    else:
    
        h_out = int(image_out.shape[0]/2) #cắt đôi biển số xe máy          
        p1_out = binary_out[0 : h_out , 0 : image_out.shape[1]]
        p2_out = binary_out[h_out : image_out.shape[0], 0 : image_out.shape[1]]
        image_p1_out = image_out[0 : h_out, 0 : image_out.shape[1]]
        image_p2_out = image_out[h_out : image_out.shape[0] , 0 : image_out.shape[1]]

        plate_info_out = find_plate_inf(p1_out, image_p1_out, 1)
        plate_info_out = plate_info_out + find_plate_inf(p2_out, image_p2_out, 5)




    # print("code response: ",response.status_code)
    print("\nplate_in <8: ",plate_info_in)
    print("\nplate_out <8: ",plate_info_out)

    url_in = "http://localhost:1994/api/Vehicle/CheckInvalid?number_plate="+plate_info_in

    url_out = "http://localhost:1994/api/Vehicle/CheckInvalid?number_plate="+plate_info_out
    payload = {}
    headers = {}

    if len(plate_info_in) >= 7:
        response_in = requests.request("GET",url_in,headers =  headers,data = payload)
        if(response_in.status_code == 200 ):
            print("code response_in: ",response_in.status_code)
            print("plate_in: ",plate_info_in)
            client.publish("rs-in", "i")
            
            # lưu hình ảnh 
            if oldPlate_in != plate_info_in:
                
                # image = "10.jpg" # Đường dẫn tới ảnh cần upload
                
                now = datetime.now()
                timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                # Các thông tin cần post lên API
                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                
                public_id  = dt_string.replace("-","").replace(":","").replace(" ","") # Public ID mà bạn muốn chỉ định cho ảnh
                print(public_id)
                
                # result = cloudinary.uploader.upload(imgData, public_id=dt_string)
                
                name = "historyImage_in.jpg"
                cv2.imwrite(name,frame_in)
                upload_result = cloudinary.uploader.upload(name, public_id=public_id, filename=public_id)
                image_url = upload_result['secure_url']
                url = "http://localhost:1994/api/History/Post"
                print(dt_string)
                data = {
                    "id_history": dt_string,
                    "isout": False,
                    "time": timestamp,
                    "image": image_url,
                    "number_plate": plate_info_in
                }
                headers = {"Content-Type": "application/json"}
                response = requests.post(url, data=json.dumps(data), headers=headers)
                if(response.status_code == 200):
                    print("POST: OK")
                else:
                    print("POST: FAILED")
            oldPlate_in = plate_info_in
            

    if len(plate_info_out) >= 7:
        response_out = requests.request("GET",url_out,headers =  headers,data = payload)
        if(response_out.status_code == 200 ):
            print("code response_in: ",response_out.status_code)
            print("plate_out: ",plate_info_out)
            client.publish("rs-out", "o")
            
            # lưu hình ảnh 
            if oldPlate_out != plate_info_out:
                
                # image = "10.jpg" # Đường dẫn tới ảnh cần upload
                
                now = datetime.now()
                timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')
                # Các thông tin cần post lên API
                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                
                public_id  = dt_string.replace("-","").replace(":","").replace(" ","") # Public ID mà bạn muốn chỉ định cho ảnh
                print(public_id)
                
                # result = cloudinary.uploader.upload(imgData, public_id=dt_string)
                
                name = "historyImage_out.jpg"
                cv2.imwrite(name,frame_out)
                upload_result = cloudinary.uploader.upload(name, public_id=public_id, filename=public_id)
                image_url = upload_result['secure_url']
                url = "http://localhost:1994/api/History/Post"
                print(dt_string)
                data = {
                    "id_history": dt_string,
                    "isout": True,
                    "time": timestamp,
                    "image": image_url,
                    "number_plate": plate_info_out
                }
                headers = {"Content-Type": "application/json"}
                response = requests.post(url, data=json.dumps(data), headers=headers)
                if(response.status_code == 200):
                    print("POST: OK")
                else:
                    print("POST: FAILED")
            oldPlate_out = plate_info_out

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.1)
cv2.destroyAllWindows()