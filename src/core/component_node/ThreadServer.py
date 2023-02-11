import threading
import socket

from src.core.component_node.NewTransaction import NewTransaction
from src.core.component_node.ThreadConnection import ThreadConnection
from src.core.component_blockchain.Blockchain import Blockchain

class ThreadServer(threading.Thread):
    def __init__(self,port_number:int,blockchain:Blockchain,new_transaction:NewTransaction):
        threading.Thread.__init__(self)
        self.port_number=port_number
        self.blockchain=blockchain
        self.new_transaction=new_transaction


    def run(self):
        host,port=("",self.port_number)
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((host,port))
        while True:
            s.listen(5)
            conn,adress=s.accept()
            print(adress)
            thread_client=ThreadConnection(blockchain=self.blockchain,conn=conn,new_transaction=self.new_transaction)
            thread_client.start()


