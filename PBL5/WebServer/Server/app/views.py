
from datetime import datetime
import cloudinary.uploader
import json
from rest_framework.response import Response 
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import status 
import requests
from .ai.webcamFindPlate import findPlate, find_plate_inf
import cv2
import urllib.request as urlrequest
import numpy as np

# Create header cloudinary here.

cloudinary.config(
  cloud_name = "damlykdtx",
  api_key = "386381942394164",
  api_secret = "mEvNmbgAMYivaAwhtpybdjsvGgk"
)
old_plate_out = None
old_plate_in = None
# show all ticket
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def start_in(request):
    number_plate, check, check_car_in = plate_detect_cam_in()
    if(check):
        if(check_car_in):
            print("state:" + str(check_car_in))
            return Response(str(number_plate), status=status.HTTP_200_OK)
        else:
            print("state:" + str(check_car_in))
            return Response(str(number_plate), status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response("", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def start_out(request):

    number_plate, check, check_car_state = plate_detect_cam_out()
    if(check):
        if(not(check_car_state)):
            print("state:" + str(check_car_state))
            return Response(str(number_plate), status=status.HTTP_401_UNAUTHORIZED)
         
        else:
            print("state:" + str(check_car_state))
            return Response(str(number_plate), status=status.HTTP_200_OK)
          
    else:
        return Response("", status=status.HTTP_400_BAD_REQUEST)

def check_state(plate_detect_number):
    url = "http://localhost:1994/api/History/CheckState?number_plate="+plate_detect_number
    payload = {}
    headers = {}
    response = requests.request("GET",url,headers =  headers,data = payload)
    state = (response.text)
    if(state=='false'):
        return 0  
    if(state=='true'):
        return 1
    else:
        return 3
    

def plate_detect_cam_in():
    global old_plate_in
    urlcam = "http://172.20.10.7/"

    fileName = 'img_cam_in.jpg'
    imgResponse = urlrequest.urlopen(urlcam+"capture")
    # Đọc dữ liệu hình ảnh từ response
    imgnP = np.array(bytearray(imgResponse.read()), dtype = np.uint8)
    frame = cv2.imdecode(imgnP, -1)
    frame_temp = frame

    isValidPlate = False

    # Capture frame-by-frame
    # cắt ảnh từ video liên tục
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    x, y, w, h = findPlate(frame)

    #lấy ảnh biển số
    image = frame[y:y+h,x:x+w]
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
   
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    # Các thông tin cần post lên API
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    
    public_id  = dt_string.replace("-","").replace(":","").replace(" ","") # Public ID mà bạn muốn chỉ định cho ảnh
                
    cv2.imwrite(fileName,frame_temp)
    cv2.imwrite("border_"+fileName,image)
    url = "http://localhost:1994/api/Vehicle/CheckInvalid?number_plate="+plate_info
    payload = {}
    headers = {}
    response = requests.request("GET",url,headers =  headers,data = payload)
    check_car_in = False
    if(response.status_code == 200 ):
        if(check_state(plate_info) != 1):
            upload_result = cloudinary.uploader.upload("border_"+fileName, public_id=public_id, filename=public_id)
            image_url = upload_result['secure_url']
            url = "http://localhost:1994/api/History/Post"
            print(dt_string)
            data = {
                "id_history": public_id,
                "isout": True,
                "time": timestamp,
                "image": image_url,
                "number_plate": plate_info
            }
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, data=json.dumps(data), headers=headers)
            old_plate_in = plate_info
            check_car_in = True
        isValidPlate = True
        
    return plate_info, isValidPlate, check_car_in


def plate_detect_cam_out():
    global old_plate_out
    urlcam = "http://172.20.10.6/"

    fileName = 'img_cam_out.jpg'
    imgResponse = urlrequest.urlopen(urlcam+"capture")
    # Đọc dữ liệu hình ảnh từ response
    imgnP = np.array(bytearray(imgResponse.read()), dtype = np.uint8)
    frame = cv2.imdecode(imgnP, -1)
    frame_temp = frame

    isValidPlate = False

    # Capture frame-by-frame
    # cắt ảnh từ video liên tục
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
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    # Các thông tin cần post lên API
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    
    public_id  = dt_string.replace("-","").replace(":","").replace(" ","") # Public ID mà bạn muốn chỉ định cho ảnh
                
    cv2.imwrite(fileName,frame_temp)
    cv2.imwrite("border_"+fileName,image)

    url = "http://localhost:1994/api/Vehicle/CheckInvalid?number_plate="+plate_info
    payload = {}
    headers = {}
    response = requests.request("GET",url,headers =  headers,data = payload)
    check_car_out = False
    if(response.status_code == 200 ):
        if(check_state(plate_info) != 0):
            old_plate_out = plate_info
            upload_result = cloudinary.uploader.upload("border_"+fileName, public_id=public_id, filename=public_id)
            image_url = upload_result['secure_url']
            url = "http://localhost:1994/api/History/Post"
            print(dt_string)
            data = {
                "id_history": public_id,
                "isout": False,
                "time": timestamp,
                "image": image_url,
                "number_plate": plate_info
            }
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, data=json.dumps(data), headers=headers)
            check_car_out = True
        isValidPlate = True
        
    return plate_info, isValidPlate, check_car_out