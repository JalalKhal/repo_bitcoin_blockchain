from time import sleep
from src.core.Transaction import Transaction
from src.core.Block import Block
from src.infrastructure.Writer import Writer
from src.globals import MINING_DIFFICULTY,INIT_BLOCK,FEES
from uuid import uuid4
from hashlib import sha512
import re
import json
from src.infrastructure.serializer import serialize




class Blockchain:

    def __init__(self):
        self.node_id = str(uuid4()).replace('-', '')
        self.nodes=set()
        self.chain=[]
        self.transactions = []
        ORIGIN_BLOCK=Block([],0,MINING_DIFFICULTY,0,init_block=INIT_BLOCK)
        self.chain.append(ORIGIN_BLOCK)

    def __str__(self):
         return json.dumps(self,default=serialize)

    def register_node(self,node_url):
        """
        Add a new node to the list of nodes
        node_url (str) format= ip_adress:port_number
        """

        pattern = re.compile(r"(localhost):(\d+)")
        match=pattern.search(node_url)
        if match:
            self.nodes.add(match.groups())
        else:
            raise Exception(f"Error during parsing: {node_url} from {self.node_id}")


    def submit_transaction(self,sender_key,receiver_key,amount,sign,transactions_prev):
        transaction=Transaction(sender_key,receiver_key,amount,FEES,sign,transactions_prev)
        self.transactions.append(transaction)


    def create_block(self):
        assert all([block.verify_block() for block in self.chain])
        block=Block(transactions=self.transactions,nonce=-1,zeros=MINING_DIFFICULTY,hashPrevBlock=self.chain[-1].hash())
        block.set_nonce(self.proof_of_work(block))
        valid=self.valid_chain(block)
        if not valid:
            sleep(3)
            self.create_block()
        else:
            self.transactions=[]
            self.chain.append(block)

    def valid_chain(self,block):
        return block.header["HashPrevBlock"] == self.chain[-1].hash()

    @classmethod
    def proof_of_work(cls,block):
        valid=False
        nonce=0
        while not valid:
            guess=(block.str_proof()+str(nonce)).encode("utf-8")
            guess_hash=sha512(guess).hexdigest()
            valid=guess_hash[:int(MINING_DIFFICULTY/8)] == "0" * int(MINING_DIFFICULTY/8) #here I have (MINING_DIFFICULTY/8)*8 (each character encoded with 8 bits)
            nonce+=1
        return nonce

    def write(self):
        writer=Writer(self,root="/home/khaldi/file.data")
        writer.write()















