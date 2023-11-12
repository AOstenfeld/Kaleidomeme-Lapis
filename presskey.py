import tkinter as tk
from time import sleep
from picamera import PiCamera

#Camera setup stuff goes here

class Screenshot:

    def __init__(self, picFile="pic#0#.jpg",vidFile = "vid#0#.h264"):
        self.picFile = picFile
        self.vidFile = vidFile

    def vid(self):
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 24

        camera.start_preview()
        camera.preview_fullscreen = False
        camera.preview.window = (300, 200, 1920, 1080)
        camera.start_recording("Videos/" + self.vidFile)
        camera.wait_recording(5)
        camera.stop_recording()
        camera.stop_preview()
        tmp = self.vidFile.split('#')
        tmp[1] = str(int(tmp[1]) + 1)
        self.vidFile = tmp[0] + '#' + tmp[1] + '#' + tmp[2]
        camera.close()

    def pic(self):
        camera = PiCamera()
        camera.resolution = (1024,768)
        camera.start_preview(alpha=200)
        sleep(2)
        camera.capture("Screenshots/" + self.picFile)
        camera.stop_preview()
        tmp = self.picFile.split('#')
        tmp[1] = str(int(tmp[1]) + 1)
        self.picFile = tmp[0] + '#' + tmp[1] + '#' + tmp[2]
        camera.close()

#GUI stuff goes here

root =  tk.Tk()

def quitCamera():
    root.destroy()

app = tk.Frame(master=root)
root.wm_title("Tkinter button")
root.geometry("320x200")
text = tk.Label(text="sample text")
text.pack()
app.pack()

shot = Screenshot()
vidbutton = tk.Button(master=app, text="Take Video", command=shot.vid)
picbutton = tk.Button(master=app, text="Take Picture", command=shot.pic)
quitbutton = tk.Button(master=app, text="Quit", command=quitCamera)
vidbutton.pack()
picbutton.pack()
quitbutton.pack()

root.mainloop()
