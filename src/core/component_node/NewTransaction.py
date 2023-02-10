import json


class NewTransaction:
    def __init__(self,node_id:int,bool_transaction:bool):
        self.node_id=node_id
        self.bool_transaction=bool_transaction
        self.count_transactions=0

    def __str__(self):
        return json.dumps(self.__dict__)
