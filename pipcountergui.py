from io import BytesIO
from time import sleep
from multiprocessing import Process, Queue

from Tkinter import *
import numpy as np

from picamera import PiCamera
import cv2
import PIL.Image
import PIL.ImageTk

from matrix_display import sub_process


camera = PiCamera()
camera.start_preview()
camera.preview.fullscreen = False
camera.preview.window = (50,50,200,200)
sleep(2)    
master = Tk()
q = Queue()
p = Process(target = sub_process, args=(q,))
p.start()
canvas = Canvas(master,width = 800,height= 600)
canvas.pack()
back1 = PIL.Image.new('RGBA', (250,187), color=(255,0,0))
back2 = PIL.Image.new('RGBA', (250,187), color=(0,255,0))
back3 = PIL.Image.new('RGBA', (250,187), color=(0,0,255))
back4 = PIL.Image.new('RGBA', (250,187), color=(128,128,0))
back5 = PIL.Image.new('RGBA', (250,187), color=(255,0,255))
imageObj1 = PIL.ImageTk.PhotoImage(image = back1)
imageObj2 = PIL.ImageTk.PhotoImage(image = back2)
imageObj3 = PIL.ImageTk.PhotoImage(image = back3)
imageObj4 = PIL.ImageTk.PhotoImage(image = back4)
imageObj5 = PIL.ImageTk.PhotoImage(image = back5)

canvasObj1 = canvas.create_image(0,0,image = imageObj1)
canvasObj2 = canvas.create_image(250,0,image = imageObj2)
canvasObj3 = canvas.create_image(500,0,image = imageObj3)
canvasObj4 = canvas.create_image(0,187,image = imageObj4)
canvasObj5 = canvas.create_image(250,187,image = imageObj5)



def count_pips(dice):
    new_dice = cv2.resize(dice, (150, 150))
    gray = cv2.cvtColor(new_dice, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    #show image
    h, w = thresh.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    
    cv2.floodFill(thresh, mask, (0,0), 255)
    cv2.floodFill(thresh, mask, (0,149), 255)
    cv2.floodFill(thresh, mask, (149, 0), 255)
    cv2.floodFill(thresh, mask, (149, 149), 255)

    params = cv2.SimpleBlobDetector_Params()
    params.filterByInertia = True
    params.minInertiaRatio = 0.5
    detector = cv2.SimpleBlobDetector_create(params)

    keypoints = detector.detect(thresh)

    return len(keypoints)


def task():
    stream = BytesIO()
    camera.capture(stream,format = 'jpeg')
    stream.seek(0)
    #print(stream)
    data = np.fromstring(stream.getvalue(),dtype=np.uint8)
    gray = cv2.imdecode(data,0)
    clone = cv2.imdecode(data,1)
    gray = cv2.blur(gray,(10,10))
    
    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    filtered = cv2.Canny(thresh, 2, 5)    
    bounded = filtered

    image, contours, hierarchy = cv2.findContours(filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    num_pips = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if (area > 7500 and area < 500000):
            x, y, w, h = cv2.boundingRect(contour)
            dice = clone[y:y+h, x:x+w]
            num_pips = num_pips + count_pips(dice)

            
            bounded = cv2.rectangle(filtered,(x,y),(x+w,y+h), (255,0,0),3)
            
    print(num_pips)
    q.put(str(num_pips))
    try:    
        im_out1 = cv2.resize(clone, (250,187))
    except: 
        print("shoot")
    try:    
        im_out2 = cv2.resize(gray, (250,187))
    except: 
        im_out2 = cv2.resize(clone, (250,187))
    try:    
        im_out3 = cv2.resize(thresh, (250,187))
    except: 
        im_out3 = cv2.resize(gray, (250,187))
    try:    
        im_out4 = cv2.resize(dice, (400,300))
    except: 
        im_out4 = cv2.resize(thresh, (400,300))
    try:    
        im_out5 = cv2.resize(bounded, (400,300))
    except: 
        im_out5 = cv2.resize(filtered, (400,300))

    image1 = PIL.Image.fromarray(im_out1)
    image2 = PIL.Image.fromarray(im_out2)
    image3 = PIL.Image.fromarray(im_out3)
    image4 = PIL.Image.fromarray(im_out4)
    image5 = PIL.Image.fromarray(im_out5)
    imageObject1 = PIL.ImageTk.PhotoImage(image = image1)
    imageObject2 = PIL.ImageTk.PhotoImage(image = image2)
    imageObject3 = PIL.ImageTk.PhotoImage(image = image3)
    imageObject4 = PIL.ImageTk.PhotoImage(image = image4)
    imageObject5 = PIL.ImageTk.PhotoImage(image = image5)

    #imageObject3 = PIL.ImageTk.PhotoImage
    canvas.delete("all")
    canvas.imageObj1 = imageObject1
    canvas.imageObj2 = imageObject2 
    canvas.imageObj3 = imageObject3    
    canvas.imageObj4 = imageObject4    
    canvas.imageObj5 = imageObject5    

    #print(imageT)
    #canvas.itemconfigure(canvasObject,image=canvas.imageObject)
    canvas.create_image(100,100,image = imageObject1)
    canvas.create_image(350,100,image = imageObject2)
    canvas.create_image(600,100,image = imageObject3)
    canvas.create_image(200,400,image = imageObject4)
    canvas.create_image(500,400,image = imageObject5)

    
    stream.flush()
    master.after(100,task)
if __name__ == '__main__':
    x = 0
    
    master.after(100,task)
    mainloop()
    camera.close()
        


