from Additional.Connection import *
from Additional.Classifier import *
from threading import Thread

def thread_run( client_name, serv, classifier, tmp_path):
    running = True
    conn = serv.get_conn_data(client_name)
    while running:
        msg = serv.recv_msg(conn)
        if msg == "IMG":
            serv.send_msg(conn, 1)
            serv.recv_file(conn, tmp_path)
            img_obj = classifier.load(tmp_path)
            res_data = classifier.classify(img_obj)
            classification_result = classifier.categorise(res_data["detections"])
            classifier.save(res_data["image_data"],"".join(tmp_path.split('.')[:-1] + ['-clf.jpg']))
            serv.send_msg(conn, classification_result)
        elif msg == "!END":
            running = False

clients = 1

server = Server()
server.add_connections(clients)
client_names = server.get_conn_names()
thread_list = []
for (ctr, client_name) in enumerate(client_names):
    clf = ObjectDetection('Additional/Dataset/')
    thread_obj = Thread(target=thread_run, args=(client_name, server, clf, 'Additional/Images/{}.jpg'.format(ctr)))
    thread_list.append(thread_obj)
    thread_obj.start()

for thread_obj in thread_list:
    thread_obj.join()

server.serv.close()
