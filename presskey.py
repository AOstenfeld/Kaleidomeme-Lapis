import tkinter as tk
from time import sleep
from picamera import PiCamera
import mods
import threading

def turn_motor(e, mot):
    while e.is_set():
        print("test")
        mot.cycle()
    e.set()

if __name__ == "__main__":
    
    root = tk.Tk()

    cam = mods.Screenshot()
    motor = mods.Motor([22, 17, 23, 27], 0.02)

    motor_on = threading.Event()
    motor_thread = threading.Thread(target=turn_motor, args=(motor_on, motor), daemon=True)
    motor_thread.start()

    app = tk.Frame(master=root)
    root.wm_title("Tkinter button")
    root.geometry("320x200")
    text = tk.Label(text="sample text")
    text.pack()
    app.pack()

    vidbutton = tk.Button(master=app, text="Take Video", command=cam.vid)
    picbutton = tk.Button(master=app, text="Take Picture", command=cam.pic)
    start_motor_button = tk.Button(master=app, text="Start Motor", command=motor_thread.run)
    stop_motor_button = tk.Button(master=app, text="Stop Motor", command=motor_on.clear)
    quitbutton = tk.Button(master=app, text="Quit", command=root.destroy)

    vidbutton.pack()
    picbutton.pack()
    start_motor_button.pack()
    stop_motor_button.pack()
    quitbutton.pack()

    root.mainloop()

    motor.clean()
    print("asdjasgdjsaghjdgasd")
