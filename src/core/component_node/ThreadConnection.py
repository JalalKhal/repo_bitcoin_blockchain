import json
import threading

from src.core.component_blockchain.Blockchain import Blockchain
from src.core.component_blockchain.Transaction import Transaction
from src.core.component_node.NewTransaction import NewTransaction


class ThreadConnection(threading.Thread):
    transaction_str=""
    def __init__(self,blockchain:Blockchain,conn,new_transaction:NewTransaction):
        threading.Thread.__init__(self)
        self.blockchain=blockchain
        self.conn=conn
        self.new_transaction=new_transaction

    def run(self):
        try:
            message=self.receive_message_from_client()
            if message[0]=="#":
                #Case of message from coordinator to tell that transaction has broadcasted to all nodes
                self.blockchain.set_transaction(Transaction(**json.loads(ThreadConnection.transaction_str))) #submit requis!
                self.new_transaction.bool_transaction=True #transaction added
                self.new_transaction.count_transactions+=1
            else:
                ThreadConnection.transaction_str=message
            self.send_response_to_client("True")
        except Exception as e:
            print(f"Error from {self.conn}:{e}")

    def receive_message_from_client(self):
        message = self.conn.recv(2048).decode() #maximum bytes received is 2048
        return message

    def send_response_to_client(self,message):
        self.conn.sendall(message.encode())





