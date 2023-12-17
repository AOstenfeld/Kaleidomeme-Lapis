import tkinter as tk
from time import sleep
import RPi.GPIO as GPIO
import mods
import threading

def motor_control():
    try:
        while not quit_event.is_set():
            if motor_on.is_set():
                motor.set_delay(1/motor_speed.get())
                motor.cycle()
            sleep(0.001)
    except tk.TclError:
        pass
    GPIO.cleanup()

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

def kill_all():
    motor_on.clear()
    quit_event.set()
    cam.close_cam()
    root.destroy()

if __name__ == "__main__":

    mot_pins = [22, 17, 23, 27]
    led_pins = [6, 26, 19]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_pins, GPIO.OUT)

    cam = mods.KalCamera()
    motor = mods.KalMotor(mot_pins, 0.02)
    rgbs = mods.KalLED(led_pins)

    quit_event = threading.Event()
    motor_on = threading.Event()

    root = tk.Tk()
    root.wm_title("Kaleidomeme controls")
    root.geometry("950x400")
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

    motor_speed = tk.Scale(master=mot_subframe, from_=10, to=100, orient=tk.HORIZONTAL)
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

    cam_label = tk.Label(master=cam_frame, text="Camera Controls", width=14, height=2, font=(None, 20, "bold"))
    cam_label.pack()

    prev_start_button = tk.Button(master=cam_frame, text="Start Preview", width=20, height=2, font=(20), command=cam.start_prev)
    prev_start_button.pack()

    prev_stop_button = tk.Button(master=cam_frame, text="Stop Preview", width=20, height=2, font=(20), command=cam.stop_prev)
    prev_stop_button.pack()

    pic_button = tk.Button(master=cam_frame, text="Take Picture", width=20, height=2, font=(20), command=lambda: take_pic(filename_input.get(1.0, "end")[:-1]))
    pic_button.pack()

    vid_button = tk.Button(master=cam_frame, text="Take Video", width=20, height=2, font=(20), command=lambda: take_vid(vid_dur.get(), filename_input.get(1.0, "end")[:-1]))
    vid_button.pack()

    cam_subframe = tk.Frame(master=cam_frame)
    cam_subframe.pack()

    dur_label = tk.Label(master=cam_subframe, text="Video\nduration (sec):", font=(20))
    dur_label.grid(row=0, column=0)

    vid_dur = tk.Scale(master=cam_subframe, from_=5, to=30, orient=tk.HORIZONTAL)
    vid_dur.grid(row=0, column=1)

    cam_subframe2 = tk.Frame(master=cam_frame)
    cam_subframe2.pack()

    file_label = tk.Label(master=cam_subframe2, text="File name:", font=(20))
    file_label.grid(row=0, column=0)

    filename_input = tk.Text(master=cam_subframe2, height=1, width=20)
    filename_input.grid(row=0, column=1)

    quit_button = tk.Button(master=root, text="Quit", width=14, height=2, font=(20), command=kill_all)
    quit_button.place(x=375, y=300)

    motor_thread = threading.Thread(target=motor_control, args=())
    motor_thread.start()

    led_thread = threading.Thread(target=led_control, args=(), daemon=True)
    led_thread.start()

    root.mainloop()

    rgbs.stop()
