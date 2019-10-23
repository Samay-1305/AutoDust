import subprocess
import platform
import socket

def get_hostname(local=False):
    cmd = 'ipconfig' if platform.system() == 'Windows' else 'ifconfig'
    res = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].decode()
    if local:
        req = "169.254"
    else:
        req = "192.168"
    if req in res:
        start = res.index(req)
        end = start + res[start:].index(' ')
        ip_address = res[start:end].strip()
        return ip_address
    else:
        print("Unable to find IP address ... Assigning to system name")
        return socket.gethostname()

class Server:
    def __init__(self, local=False):
        self.server_data = {"host":get_hostname(local),
                            "port":8080,
                            "connections":[]}
        self.serv = socket.socket()
        self.serv.bind((self.server_data["host"], self.server_data["port"]))

    def add_connections(self, no_of_conn=1):
        print("Server {} is listening on port {}".format(self.server_data["host"], self.server_data["port"]))
        for i in range(no_of_conn):
            self.serv.listen(3)
            conn, (ip_addr, port) = self.serv.accept()
            conn_data = {"ip address":ip_addr,
                         "port":port,
                         "conn":conn,
                         "name":conn.recv(128).decode()}
            self.server_data["connections"].append(conn_data)
    
    def get_conn_names(self):
        return [conn_data["name"] for conn_data in self.server_data["connections"]]

    def get_conn_data(self, name=''):
        for conn_data in self.server_data["connections"]:
            if conn_data["name"] == name:
                return conn_data
        else:
            return ''

    def send_msg(self, conn_data, text=''):
        conn_data["conn"].send(str(text).encode('UTF-8'))
        print("Message sent")

    def recv_msg(self, conn_data, size=1024):
        return conn_data["conn"].recv(size).decode()
            
    def send_file(self, conn_data, file_path, byte_size=2048):
        file_size = len(file_data)
        conn_data["conn"].send("SZ:{}".format(file_size).encode('UTF-8'))
        conn_data["conn"].recv(1)
        for i in range(0, file_size, byte_size):
            conn_data["conn"].send(file_data[i:i+byte_size])
            conn_data["conn"].recv(1).decode()
        conn_data["conn"].send(file_data[i+byte_size:])
        conn_data["conn"].recv(1).decode()
        print("File sent")

    def recv_file(self, conn_data, file_path, byte_size=2048):
        file_size = int(conn_data["conn"].recv(512).decode().split(':')[-1])
        print(file_size)
        conn_data["conn"].send(b'1')
        file_data = b''
        for i in range(0, file_size, byte_size):
            file_data += conn_data["conn"].recv(byte_size)
            conn_data["conn"].send(b'1')
        with open(file_path, 'wb+') as file_object:
            file_object.write(file_data)
        print("File recieved")
