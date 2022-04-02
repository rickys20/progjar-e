from importlib.resources import is_resource
import socket
import logging
import json
import ssl
import threading

alldata = dict()

alldata['1']=dict(nomor=1, nama="Keylor Navas", posisi="GK 1")
alldata['2']=dict(nomor=2, nama="Donnaruma", posisi="GK 2")
alldata['3']=dict(nomor=3, nama="Marquinhos ", posisi="CB 3")
alldata['4']=dict(nomor=4, nama="Sergio Ramos", posisi="CB 4")
alldata['5']=dict(nomor=5, nama="Kipembe", posisi="CB 5")
alldata['6']=dict(nomor=6, nama="Lionel Messi", posisi="RW 6")
alldata['7']=dict(nomor=7, nama="Neymar Jr", posisi="LW 7")
alldata['8']=dict(nomor=8, nama="Kylian Mbappe", posisi="CF 8")
alldata['9']=dict(nomor=9, nama="Mauro Icardi", posisi="CF 9")
alldata['10']=dict(nomor=10, nama="Ander Herrera", posisi="CM 10")
alldata['11']=dict(nomor=11, nama="Adama Traure", posisi="RW 11")
alldata['12']=dict(nomor=12, nama="Aubameyang", posisi="CF 12")
alldata['13']=dict(nomor=13, nama="Pedri", posisi="CM 13")
alldata['14']=dict(nomor=14, nama="Marco Verrati", posisi="CM 14")
alldata['15']=dict(nomor=15, nama="Marcello", posisi="RB 15")
alldata['16']=dict(nomor=16, nama="Ronaldo", posisi="CF 16")
alldata['17']=dict(nomor=17, nama="Harry Maguire", posisi="CB 17")
alldata['18']=dict(nomor=18, nama="De Gea", posisi="GK 18")
alldata['19']=dict(nomor=19, nama="Harry Kane", posisi="CF 19")
alldata['20']=dict(nomor=20, nama="Coutinho", posisi="CM 20")
alldata['21']=dict(nomor=21, nama="Saudio Mane", posisi="CF 21")
alldata['22']=dict(nomor=22, nama="M Salah", posisi="CF 22")

def versi():
    return "versi 0.0.1"


def proses_request(request_string):
    #format request
    # NAMACOMMAND spasi PARAMETER
    cstring = request_string.split(" ")
    hasil = None
    try:
        command = cstring[0].strip()
        if (command == 'getdatapemain'):
            # getdata spasi parameter1
            # parameter1 harus berupa nomor pemain
            logging.warning("getdata")
            nomorpemain = cstring[1].strip()
            try:
                logging.warning(f"data {nomorpemain} ketemu")
                hasil = alldata[nomorpemain]
            except:
                hasil = None
        elif (command == 'versi'):
            hasil = versi()
    except:
        hasil = None
    return hasil


def serialisasi(a):
    #print(a)
    #serialized = str(dicttoxml.dicttoxml(a))
    serialized =  json.dumps(a)
    logging.warning("serialized data")
    logging.warning(serialized)
    return serialized

def run_server(server_address):
    #--- INISIALISATION ---
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    logging.warning(f"starting up on {server_address}")
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1000)
    
    threads = dict()
    thread_index = 0

    while True:
        # Wait for a connection
        logging.warning("waiting for a connection")
        connection, client_address = sock.accept()
        logging.warning(f"Incoming connection from {client_address}")
        # Receive the data in small chunks and retransmit it

        try:

            threads[thread_index] = threading.Thread(
                target=send_d, args=(client_address, connection))
            threads[thread_index].start()
            thread_index += 1

            # Clean up the connection
        except ssl.SSLError as error_ssl:
            logging.warning(f"SSL error: {str(error_ssl)}")
            
def send_d(client_address, connection):
    selesai = False
    data_received = ""  # string
    while True:
        data = connection.recv(32)
        logging.warning(f"received {data}")
        if data:
            data_received += data.decode()
            if "\r\n\r\n" in data_received:
                selesai = True

            if (selesai != False):
                hasil = proses_request(data_received)
                logging.warning(f"hasil proses: {hasil}")

                hasil = serialisasi(hasil)
                hasil += "\r\n\r\n"
                connection.sendall(hasil.encode())
                selesai = False
                data_received = ""  # string
                break

        else:
            logging.warning(f"no more data from {client_address}")
            break

if __name__=='__main__':
    try:
        run_server(('0.0.0.0', 12000), is_secure=false)
    except KeyboardInterrupt:
        logging.warning("Control-C: Program berhenti")
        exit(0)
    finally:
        logging.warning("selesai")