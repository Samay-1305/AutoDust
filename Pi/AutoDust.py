#from picamera import PiCamera
from time import sleep
import os
from Additional.Connection import Client
from Additional.Interface import Control

device_name = "Dustbin"

host = "192.168.0.173"
port = 8080

file_path = 'Additional/Images/image.jpg'

#camera = PiCamera()
#camera.start_preview()
sleep(1)

controller = Control()

conn = Client(device_name)
conn.connect(host, port)

running = True
while running:
    try:
        controller.listen_for_change()
        sleep(0.5)
        os.system("fswebcam -r 1240x720-v -S 10 --set brightness=50% {}".format(file_path))
        #camera.capture(file_path)
        conn.send_msg("IMG")
        conn.recv_msg(1)
        conn.send_file(file_path)
        action = conn.recv_msg()
        print(action)
       	res = controller.rotate(action)
        if not(res):
            raise SystemError

    except Exception as err:
        print(err)
        conn.send_msg("!END")
        controller.release()
        #camera.stop_preview()
        running = False

