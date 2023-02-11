import threading
import socket

class ThreadClient(threading.Thread):
    def __init__(self,port_number:int,data:str):
        threading.Thread.__init__(self)
        self.port_number=port_number
        self.data=data
        self.ack=False

    def run(self):
        host,port=("localhost",self.port_number)
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            s.connect((host,port))
            data=self.data.encode("utf-8")
            s.sendall(data)
            ack=s.recv(1024).decode()
            assert ack=="False" or ack == "True"
            if ack=="True":
                self.ack=True
        except ConnectionRefusedError:
            print(f"Connection refused for server{self.port_number}")
        finally:
            s.close()

