from io import BytesIO
import PIL.Image
import PIL.ImageTk
from Tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview()

camera.preview.fullscreen = False
camera.preview.window = (50,50,200,200)
sleep(2)
master = Tk()

canvas = Canvas(master,width = 800,height= 600)
#I don't think this does anything
canvas.pack()
back = PIL.Image.new('RGBA', (800,600), color=(255,0,0))
imageObject = PIL.ImageTk.PhotoImage(image = back)
canvasObject = canvas.create_image(0,0, anchor = 'nw',image = imageObject)  

def task():
    stream = BytesIO()
    camera.capture(stream,format = 'jpeg')
    stream.seek(0)
    print(stream)
    test = PIL.Image.open(stream)
    test.thumbnail([800,600])
    image = PIL.ImageTk.PhotoImage(test)
    #test = PIL.Image.new('RGBA', (800,600), color=(0,255,0))
    #imageObject = PIL.ImageTk.PhotoImag e(image = test)
    canvas.itemconfigure(canvasObject,image=image)
    ##canvas.itemconfig(,image = image)
    stream.flush()
    master.after(2000,task) 

master.after(2000,task)
mainloop()
master.quit()


