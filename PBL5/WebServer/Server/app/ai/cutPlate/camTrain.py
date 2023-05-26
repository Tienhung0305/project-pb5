import cv2
import time
from datetime import datetime
import requests
from camTrainFunc import findPlate, find_plate_inf

video_capture = cv2.VideoCapture(0)
i = 0
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    x, y, w, h = findPlate(frame)
    
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    image=frame[y:y+h,x:x+w]
    if w/h > 2:
        image = cv2.resize(image, (470, 110))# 0:h
        
    else:
        image = cv2.resize(image, (315, 235))
    
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (3,3), 0) # lam mo de giam gay nhieu
    # Ap dung threshold de phan tach so va nen
    binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    if w/h > 2:
        plate_info = find_plate_inf(binary, image, i);
        
    else:
    
        h = int(image.shape[0]/2)
        p1 = binary[0:h,0:image.shape[1]]
        p2 = binary[h:image.shape[0],0:image.shape[1]]
        image_p1 = image[0:h,0:image.shape[1]]
        image_p2 = image[h:image.shape[0],0:image.shape[1]]
        
        plate_info = find_plate_inf(p1, image_p1, i)
        plate_info = plate_info + find_plate_inf(p2, image_p2, i + 5)

    i = i + 9    

    print("biển số: ",plate_info)
   

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
     # Display the resulting frame
    cv2.imshow('Video', frame)
    time.sleep(0.1)
#client.loop_forever()
video_capture.release()
cv2.destroyAllWindows()




