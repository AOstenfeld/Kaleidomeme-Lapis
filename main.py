import tkinter as tk
from time import sleep
import mods
import threading

def motor_control():
    while not quit_event.is_set():
        if motor_on.is_set():
            motor.set_delay(motor_speed.get()/1000)
            motor.cycle()
        sleep(0.001)

def take_pic(filename):
    pic_thread = threading.Thread(target=cam.pic, args=(filename, ))
    pic_thread.start()
    pic_thread.join()

def take_vid(dur, filename):
    vid_thread = threading.Thread(target=cam.vid, args=(dur, filename))
    vid_thread.start()

def  kill_all():
    quit_event.set()
    root.destroy()

if __name__ == "__main__":

    root = tk.Tk()

    cam = mods.KalCamera()
    motor = mods.Motor([22, 17, 23, 27], 0.02)

    quit_event = threading.Event()
    motor_on = threading.Event()
    motor_thread = threading.Thread(target=motor_control, args=(), daemon=True)
    motor_thread.start()

    app = tk.Frame(master=root)
    root.wm_title("Kaleidomeme controls")
    root.geometry("320x320")
    app.pack()

    pic_button = tk.Button(master=app, text="Take Picture", command=lambda: take_pic(filename_input.get(1.0, "end")))
    filename_input = tk.Text(master=app, height=1, width=20)
    vid_button = tk.Button(master=app, text="Take Video", command=lambda: take_vid(5, None))
    start_motor_button = tk.Button(master=app, text="Start Motor", command=motor_on.set)
    motor_speed = tk.Scale(master=root, from_=20, to=5, orient=tk.HORIZONTAL)
    stop_motor_button = tk.Button(master=app, text="Stop Motor", command=motor_on.clear)
    quit_button = tk.Button(master=app, text="Quit", command=kill_all)

    pic_button.pack()
    filename_input.pack()
    vid_button.pack()
    start_motor_button.pack()
    motor_speed.pack()
    stop_motor_button.pack()
    quit_button.pack()

    root.mainloop()

    motor.clean()
