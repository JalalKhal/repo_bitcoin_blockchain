from threading import current_thread
from src.core.component_blockchain.Transaction import Transaction
from src.core.component_blockchain.Block import Block
from src.infrastructure.Writer import Writer
from src.globals import MINING_DIFFICULTY,INIT_BLOCK
import json
from src.infrastructure.serializer import serialize




class Blockchain:

    def __init__(self):

        self.chain=[]
        self.transactions = []
        ORIGIN_BLOCK=Block([],MINING_DIFFICULTY,0,init_block=INIT_BLOCK)
        self.chain.append(ORIGIN_BLOCK)

    def __str__(self):
         return json.dumps(self,default=serialize)




    def submit_block(self,block):
        assert all([block.verify_block() for block in self.chain])
        valid=self.valid_chain(block)
        if not valid:
            raise Exception(f"block {block} from thread {current_thread().name} is not valid ! ")
        self.chain.append(block)
        self.transactions=[]

    def create_block_proof(self,hashPrevBlock,zeros=MINING_DIFFICULTY):
        return Block(transactions=self.transactions,zeros=zeros,hashPrevBlock=hashPrevBlock)

    def set_transaction(self,transaction):
        assert isinstance(transaction,Transaction)
        assert transaction.verify_transaction()
        self.transactions.append(transaction)


    def valid_chain(self,block):
        return block.header["HashPrevBlock"] == self.chain[-1].hash()


    def write(self,file_path="blockchain.data",mode="a"):
        writer=Writer(self,dict_method={"file_path":file_path})
        writer.write(mode=mode)















