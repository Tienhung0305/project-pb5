
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
    number_plate, check, check_car_state = plate_detect_cam_in()
    check_car_in = check_state(number_plate)
    if(check):
        return Response(str(number_plate), status=status.HTTP_200_OK)
    else:
        return Response("", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def start_out(request):
    number_plate, check, check_car_state_out = plate_detect_cam_out()
    check_car_state = check_state(number_plate)
    if(check):
        return Response(str(number_plate), status=status.HTTP_200_OK)
    else:
        return Response("", status=status.HTTP_400_BAD_REQUEST)

def check_state(plate_detect_number):
    url = "http://localhost:1994/api/Parking/CheckState?number_plate="+plate_detect_number
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
    

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def get_slot_parking(request):
    url = "http://localhost:1994/api/Parking/GetNumberParked"
    payload = {}
    headers = {}
    response = requests.request("GET",url,headers =  headers,data = payload)
    state = (response.text)
    print(state)
    return Response(int(state), status=status.HTTP_200_OK)

    

def plate_detect_cam_in():
    global old_plate_in
    urlcam = "http://192.168.6.84/capture"

    fileName = 'img_cam_in.jpg'
    imgResponse = urlrequest.urlopen(urlcam)
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
    check_state_car = False;
    if(response.status_code == 200 ):
        check_state_code = check_state(plate_info)
        if(check_state_code  == 1):
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

            url_post = "http://localhost:1994/api/Parking/Post"
            data_post = {
                "number_plate": plate_info
            }
            headers_post = {"Content-Type": "application/json"}
            response_post = requests.post(url_post, data=json.dumps(data_post), headers=headers_post)
            check_state_car = True;
            old_plate_in = plate_info
        isValidPlate = True
        
    return plate_info, isValidPlate, check_state_car


def plate_detect_cam_out():
    global old_plate_out
    urlcam = "http://192.168.6.75/"

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
    check_car_state = False
    if(response.status_code == 200 ):
        if(check_state(plate_info) == 0):
            old_plate_out = plate_info
            upload_result = cloudinary.uploader.upload("border_"+fileName, public_id=public_id, filename=public_id)
            image_url = upload_result['secure_url']
            url_out = "http://localhost:1994/api/History/Post"
            print(dt_string)
            data_out = {
                "id_history": public_id,
                "isout": False,
                "time": timestamp,
                "image": image_url,
                "number_plate": plate_info
            }
            headers_out = {"Content-Type": "application/json"}
            response_out = requests.post(url_out, data=json.dumps(data_out), headers=headers_out)
            url_delete = "http://localhost:1994/api/Parking/Delete?number_plate="+plate_info
            response_delete = requests.delete(url_delete)
            check_car_state = True
        isValidPlate = True
        
    return plate_info, isValidPlate, check_car_state