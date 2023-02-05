from hashlib import sha512
import json
from src.globals import INIT_TRANSACTION


class Transaction:

    def __init__(self,\
        sender_key:tuple,receiver_key:tuple,amount:float,fees:float,sign:int,transactions:list=INIT_TRANSACTION):
        """
        :param sender_key: public key of sender
        :param receiver_key: public key of receiver
        :param amount: amount of transaction
        :param fees: fees of transaction
        :param sign: int represent signature
        :param transactions: list of transactions t which t.receiver_key=self.sender_key if transactions set by user
        """
        (ns,ds)=sender_key
        (nr,dr)=receiver_key
        assert ns>0 and nr >0 and ds > 0 and dr >0
        self.transactions=transactions
        self.sender_key=sender_key
        self.receiver_key=receiver_key
        self.amount=amount
        self.fees=fees
        self.sign=sign
        assert fees >=0 and amount>=0
        assert self.verify_transaction_signature() and self.verify_transaction_amount()

    def __str__(self):
        return json.dumps({"Transactions":self.transactions,"Sender key":self.sender_key,\
        "Receiver key":self.receiver_key,"Amount":self.amount,"Fees":self.fees,"Signature":self.sign},default=str)


    def verify_transaction_amount(self):
        """
        :return: boolean that show if sender have enough bitcoin to send them.
        """
        if self.transactions==INIT_TRANSACTION:
            return True
        total_amount=0
        for t in self.transactions:
            if t.receiver_key != self.sender_key:
                return False
            total_amount+=t.amount
        return total_amount >= self.amount + self.fees

    def verify_transaction_signature(self):
        transaction_wo_sign=json.dumps({"Transactions":self.transactions,"Sender key":self.sender_key, \
        "Receiver key":self.receiver_key,"Amount":self.amount,"Fees":self.fees},default=str)
        msg=transaction_wo_sign
        hashMsg = int.from_bytes(sha512(msg.encode("utf-8")).digest(), byteorder='big')
        hashFromSign=pow(self.sign,self.sender_key[1], self.sender_key[0]) #pow(signature,d,n)
        return hashMsg==hashFromSign








