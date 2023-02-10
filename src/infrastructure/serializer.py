from src.globals import INIT_TRANSACTION


def serialize(obj):
    from src.core.component_blockchain.Transaction import Transaction
    from src.core.component_blockchain.Block import Block
    from src.core.component_blockchain.Blockchain import Blockchain


    if isinstance(obj, Transaction):
        if obj.transactions == INIT_TRANSACTION:
            return obj.__dict__
        else:
            dict_transac = {
                "transactions": [serialize(t) for t in obj.transactions],
                "sender_key": obj.sender_key,
                "receiver_key": obj.receiver_key,
                "amount": obj.amount,
                "fees": obj.fees,
                "sign": obj.sign
            }
            return dict_transac

    if isinstance(obj,Block):
        return {
            "transactions":[serialize(t) for t in obj.transactions],
            "transaction_counter":obj.transaction_counter,
            "header":obj.header
        }

    if isinstance(obj,Blockchain):
        return {
            "chain": [serialize(c) for c in obj.chain],
            "transactions": [serialize(t) for t in obj.transactions]
        }


