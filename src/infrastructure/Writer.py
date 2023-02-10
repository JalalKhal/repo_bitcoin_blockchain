class Writer:
    def __init__(self,data:object,method:str="disk local file",dict_method:dict={"file_path":"file.data"}):
        self.dict_method=dict_method
        self.method=method
        self.data=data

    def write(self,mode="a"):
        if self.method == "disk local file":
            with open(self.dict_method["file_path"],mode) as f:
                f.write(str(self.data))
