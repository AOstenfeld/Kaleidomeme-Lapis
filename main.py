import tkinter as tk
from time import sleep
import RPi.GPIO as GPIO
import mods
import threading

def motor_control():
    while not quit_event.is_set():
        if motor_on.is_set():
            motor.set_delay(motor_speed.get()/1000)
            motor.cycle()
        sleep(0.001)

def led_control():
    rgbs.start()
    try:
        while not quit_event.is_set():
            rgbs.set_dc(red_level.get(), green_level.get(), blue_level.get())
            sleep(0.001)
    except tk.TclError:
        pass

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

    mot_pins = [22, 17, 23, 27]
    led_pins = [6, 27, 22]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(mot_pins, GPIO.OUT)
    GPIO.setup(led_pins, GPIO.OUT)

    cam = mods.KalCamera()
    motor = mods.KalMotor(mot_pins, 0.02)
    rgbs = mods.KalLED(led_pins)

    quit_event = threading.Event()
    motor_on = threading.Event()

    root = tk.Tk()
    root.wm_title("Kaleidomeme controls")
    root.geometry("900x300")
    root.resizable(False, False)

    mot_frame = tk.Frame(master=root, highlightbackground="black", highlightthickness=2)
    mot_frame.place(x=10, y=10)

    led_frame = tk.Frame(master=root, highlightbackground="black", highlightthickness=2)
    led_frame.place(x=350, y=10)

    cam_frame = tk.Frame(master=root, highlightbackground="black", highlightthickness=2)
    cam_frame.place(x=650, y=10)

    mot_label = tk.Label(master=mot_frame, text="Motor Controls", width=14, height=2, font=(None, 20, "bold"))
    mot_label.pack()
    
    start_motor_button = tk.Button(master=mot_frame, text="Start Motor", width=20, height=2, font=(20), command=motor_on.set)
    start_motor_button.pack()
    
    stop_motor_button = tk.Button(master=mot_frame, text="Stop Motor", width=20, height=2, font=(20), command=motor_on.clear)
    stop_motor_button.pack()

    mot_subframe = tk.Frame(master=mot_frame)
    mot_subframe.pack()

    speed_label = tk.Label(master=mot_subframe, text="Motor Speed:", font=(20))
    speed_label.grid(row=0, column=0)

    motor_speed = tk.Scale(master=mot_subframe, from_=20, to=5, orient=tk.HORIZONTAL)
    motor_speed.grid(row=0, column=1)

    led_label = tk.Label(master=led_frame, text="LED Controls", font=(None, 24, "bold"))
    led_label.pack()

    led_subframe = tk.Frame(master=led_frame)
    led_subframe.pack()

    red_label = tk.Label(master=led_subframe, text="Red:", font=(20))
    red_label.grid(row=0, column=0)
    
    red_level = tk.Scale(master=led_subframe, from_=0, to=100, orient=tk.HORIZONTAL)
    red_level.grid(row=0, column=1)

    green_label = tk.Label(master=led_subframe, text="Green:", font=(20))
    green_label.grid(row=1, column=0)
    
    green_level = tk.Scale(master=led_subframe, from_=0, to=100, orient=tk.HORIZONTAL)
    green_level.grid(row=1, column=1)

    blue_label = tk.Label(master=led_subframe, text="Blue:", font=(20))
    blue_label.grid(row=2, column=0)
    
    blue_level = tk.Scale(master=led_subframe, from_=0, to=100, orient=tk.HORIZONTAL)
    blue_level.grid(row=2, column=1)

    pic_button = tk.Button(master=cam_frame, text="Take Picture", command=lambda: take_pic(filename_input.get(1.0, "end")))
    pic_button.pack()

    vid_button = tk.Button(master=cam_frame, text="Take Video", command=lambda: take_vid(5, None))
    vid_button.pack()

    filename_input = tk.Text(master=cam_frame, height=1, width=20)
    filename_input.pack()
    
    quit_button = tk.Button(master=cam_frame, text="Quit", command=kill_all)
    quit_button.pack()

    motor_thread = threading.Thread(target=motor_control, args=(), daemon=True)
    motor_thread.start()

    led_thread = threading.Thread(target=led_control, args=(), daemon=True)
    led_thread.start()

    root.mainloop()

    rgbs.stop()
    GPIO.cleanup()
