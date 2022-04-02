import socket
import json
import logging
import threading
import datetime
import random
from tabulate import tabulate

server_address = ('172.16.16.101', 12000)

def make_socket(destination_address='localhost',port=12000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        return sock
    except Exception as ee:
        logging.warning(f"error {str(ee)}")

def deserialisasi(s):
    logging.warning(f"deserialisasi {s.strip()}")
    return json.loads(s)

def send_command(command_str):
    alamat_server = server_address[0]
    port_server = server_address[1]
    sock = make_socket(alamat_server,port_server)

    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = deserialisasi(data_received)
        logging.warning("data received from server:")
        return hasil
    except Exception as ee:
        logging.warning(f"error during data receiving {str(ee)}")
        return False

def getdatapemain(nomor=0):
    cmd=f"getdatapemain {nomor}\r\n\r\n"
    hasil = send_command(cmd)
    if (hasil):
        pass
    else:
        print("kegagalan pada data transfer")
    return hasil

def lihatversi():
    cmd=f"versi \r\n\r\n"
    hasil = send_command(cmd)
    return hasil
    
def req_multithread(total_request, table_hasil):
    texec = dict()
    t_start = datetime.datetime.now()
    total_response = 0

    #    Multithreading
    for k in range(total_request):
        texec[k] = threading.Thread(
            target=getdatapemain, args=(random.randint(1, 20),))
        texec[k].start()

    for k in range(total_request):
         if (texec[k]):
            total_response += 1
            texec[k].join()

    t_end = datetime.datetime.now()

    print(f"Waktu_Selesai: {t_end - t_start}")
    table_hasil.append([total_request, total_request, total_response, t_end-t_start])

if __name__ == '__main__':
    h = lihatversi()
    if (h):
        print(h)
    total_request = [1, 5, 10, 20]
    array_data = []
    
    for request in total_request:
        req_multithread(request, array_data)

        
    t_header = ["Thread Count", "Request Count", "Response Count", "time"]
    print(tabulate(array_data, headers=t_header, tablefmt="fancy_grid"))