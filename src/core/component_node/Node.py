import json
import threading
from hashlib import sha512
from queue import Queue
from time import sleep
from Crypto.PublicKey import RSA
from src.core.component_blockchain.Transaction import Transaction
from src.core.component_node.NewTransaction import NewTransaction
from src.globals import PORT_BEGIN, FEES, INIT_TRANSACTION, N, TIMEOUT, MINING_DIFFICULTY
from src.core.component_node.ThreadServer import ThreadServer
from src.core.component_node.ThreadClient import ThreadClient

from src.core.component_blockchain.Blockchain import Blockchain

class Node(threading.Thread):
    number_nodes=N
    def __init__(self, id, thread_flask: threading.Thread, q:Queue, lock: threading.Lock):
        super().__init__()
        self.id=id
        self.port_number=PORT_BEGIN+id
        self.blockchain=Blockchain()
        self.new_transaction=NewTransaction(self.id,False)
        self.thread_server=ThreadServer(port_number=self.port_number,blockchain=self.blockchain,new_transaction=self.new_transaction)
        self.thread_flask=thread_flask
        self.q=q
        self.lock=lock
        self.control_freq_transaction=False
        self.list_user_input=[]
        self.coord=None



    def run(self):
        self.thread_server.start()
        sleep(3)
        thread_listen_user_input=threading.Thread(target=self.listen_user_input)
        thread_listen_user_input.start()

        thread_handle_transaction=threading.Thread(target=self.handle_transaction)
        thread_handle_transaction.start()

        thread_submit_block=threading.Thread(target=self.create_block)
        thread_submit_block.start()


    def create_block(self):
        while True:
            sleep(1)
            if self.new_transaction.bool_transaction:
                #new transaction
                block=self.blockchain.create_block_proof(self.blockchain.chain[-1].hash())
                valid=False
                noncel=0
                remote_nonce=False
                while not valid:
                    if not self.q.empty():
                        noncer=self.q.get()
                        nonce=noncer
                        remote_nonce=True
                    else:
                        noncel+=1
                        nonce=noncel
                    guess=(block.str_proof()+str(nonce)).encode("utf-8")
                    guess_hash=sha512(guess).hexdigest()
                    valid=guess_hash[:int(MINING_DIFFICULTY/8)] == "0" * int(MINING_DIFFICULTY/8) #here I have (MINING_DIFFICULTY/8)*8 (each character encoded with 8 bits)
                    if valid == True:
                        if remote_nonce==False:
                            with self.lock:
                                if self.q.empty():
                                    self.q.put(nonce)
                                else:
                                    nonce=self.q.get()

                        break
                block.set_nonce(nonce)
                self.blockchain.submit_block(block)
                self.new_transaction.bool_transaction=False
                self.blockchain.write(file_path=f"noeud{self.id}_blockchain.json",mode="w")
                if int(self.coord)==int(self.id):
                    self.list_user_input.pop(0)
                    self.thread_flask.back["blockchain"]=self.blockchain
                    self.thread_flask.back["nonce"]=nonce
                    sleep(3) # wait for others threads to finished to add block to blockchain
                    self.control_freq_transaction=False


    def listen_user_input(self):
        while True:
            sleep(0.5)
            user_input=self.thread_flask.user_input
            if user_input:
                self.coord=user_input[0]
                if user_input[1]:
                    if int(self.id)==int(self.coord):
                        self.list_user_input.append(user_input)
                        self.thread_flask.user_input=self.thread_flask.user_input[0],None

    def handle_transaction(self):
        while True:
            sleep(1)
            if self.coord:
                if int(self.id)==int(self.coord):
                    while self.control_freq_transaction:
                        sleep(1)#process at this moment for another user input or beginning
                    if len(self.list_user_input):
                        self.control_freq_transaction=True
                        user_input=self.list_user_input[0]
                        coordinator,amount=user_input
                        transaction=self.create_transaction(int(amount))
                        self.broadcast_message(str(transaction))
                        self.broadcast_message(f"#OK for transaction#:{str(transaction)}")
                        self.blockchain.set_transaction(transaction)
                        self.new_transaction.count_transactions+=1
                        self.new_transaction.bool_transaction=True




    def broadcast_message(self,message:str) -> bool:
        timeout=0
        sends={i:self.send(PORT_BEGIN+i,str(message)) for i in range(self.number_nodes) if i != self.id}
        while not all(sends.values()) and timeout < TIMEOUT:
            sends={i:self.send(PORT_BEGIN+i,str(message)) for i in range(self.number_nodes) if i != self.id}
            timeout+=1
        if not all(sends.values()) and timeout == TIMEOUT:
            raise Exception(f"Sending message to all nodes from {self.id} failed:{sends}")
        #all(sends.values()) is True
        return True



    def send(self,port_number,data:str):
        thread_client=ThreadClient(port_number,data)
        thread_client.start()
        thread_client.join()
        return thread_client.ack


    def create_transaction(self,amount,transactions=INIT_TRANSACTION):
        keyPair_sender=RSA.generate(bits=1024)
        keyPair_receiver=RSA.generate(bits=1024)
        s=keyPair_sender.n,keyPair_sender.e
        r=keyPair_receiver.n,keyPair_receiver.e
        fees=FEES
        transaction_wo_sign=json.dumps({"Transactions":transactions,"Sender key":s, \
                                "Receiver key":r,"Amount":amount,"Fees":fees},default=str)
        hash=int.from_bytes(sha512(transaction_wo_sign.encode("utf-8")).digest(),byteorder="big")
        signature=pow(hash,keyPair_sender.d,keyPair_sender.n)
        return Transaction(s,r,amount,FEES,signature,transactions)
















