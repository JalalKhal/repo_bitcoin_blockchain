class Writer:
    def __init__(self,data:object,method:str="disk local file",root:str="file.data"):
        self.root=root
        self.method=method
        self.data=data

    def write(self):
        if self.method == "disk local file":
            with open(self.root,"a") as f:
                f.write(str(self.data))
