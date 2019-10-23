from Additional.Connection import Client

device_name = "Display"

host = "192.168.0.173"
port = 8080

file_path = 'Additional/Images/image.jpg'

conn = Client(device_name)
conn.connect(host, port)

#Req = raw_image, classified_image, category