import json
from hashlib import sha512
import random
from Crypto.PublicKey import RSA
from src.core.component_blockchain.Blockchain import Blockchain
from src.core.component_blockchain.Transaction import Transaction
from src.globals import INIT_TRANSACTION,FEES,PORT_BEGIN

if __name__=="__main__":
    blockchain=Blockchain(("localhost",PORT_BEGIN))
    for i in range(101):
        blockchain.register_node(f"localhost:{str(i+10000)}")
        print(f"Test for registering node {i+1}:OK")

    for i in range(101):
        keyPair_sender=RSA.generate(bits=1024)
        keyPair_receiver=RSA.generate(bits=1024)
        s=keyPair_sender.n,keyPair_sender.e
        r=keyPair_receiver.n,keyPair_receiver.e
        amount=10
        fees=FEES
        transaction_wo_sign=json.dumps({"Transactions":INIT_TRANSACTION,"Sender key":s, \
                                        "Receiver key":r,"Amount":amount,"Fees":FEES},default=str)
        msg=transaction_wo_sign.encode("utf-8")
        hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
        signature=pow(hash,keyPair_sender.d,keyPair_sender.n)
        t=Transaction(s,r,amount,fees,signature)
        amount=random.random()
        sender=r
        receiver=s
        fees=FEES
        transaction_wo_sign=json.dumps({"Transactions":[t],"Sender key":sender, \
                                        "Receiver key":receiver,"Amount":amount,"Fees":fees},default=str)
        msg=transaction_wo_sign.encode("utf-8")
        hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
        signature=pow(hash,keyPair_receiver.d,keyPair_receiver.n)
        t1=Transaction(sender,receiver,amount,fees,signature,transactions=[t])
        blockchain.submit_transaction(sender,receiver,amount,signature,[t])
        blockchain.create_block()
    blockchain.write()

