import json
from src.core.Transaction import Transaction
from hashlib import sha512
class Block:

    def __init__(self,transactions:list[Transaction],nonce:int,zeros,hashPrevBlock:int,init_block=False):
        """
        :param transactions: list of immutable transaction
        :param nonce: nonce for Proof of Work
        :param hashPrevBlock: hash of previous block
        :param zeros: number of zeros for resolve Proof of Work
        """
        if init_block==False:
            self.transactions=transactions
            self.transaction_counter=len(transactions)
            self.header={
                "HashPrevBlock":hashPrevBlock,
                "Nonce":nonce,
                "Zeros":zeros
            }
            assert self.verify_integrity_transactions()
        else:
            self.transactions=[]
            self.transaction_counter=0
            self.header={
            }


    def __str__(self):
        return json.dumps({"Transactions":self.transactions,"Transaction Counter":self.transaction_counter,\
                "Header":self.header},default=str)

    def str_proof(self):
        header_wo_nonce=self.header.copy()
        del header_wo_nonce["Nonce"]
        return json.dumps({"Transactions":self.transactions,"Transaction Counter":self.transaction_counter, \
                           "Header":header_wo_nonce},default=str)

    def verify_integrity_transactions(self):
        """
        :return: verify if block is not corrupted
        """
        valid=True
        for t in self.transactions:
            valid=valid and isinstance(t,Transaction)
        return valid

    def hash(self):
        return int.from_bytes(sha512(str(self).encode("utf-8")).digest(), byteorder='big')

    def set_nonce(self,nonce):
        self.header["Nonce"]=nonce








