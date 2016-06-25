#coding=utf-8
import pdb
status_collection = {
    0 : "error" ,
    1 : "success" ,
    2 : "exist" ,
    3 : "not exist" ,
    4 : "not id" ,
    5 : "params error" ,
    
}

class Status :
    ERROR = 0
    OK = 1
    EXIST = 2
    NOT_EXIST = 3
    NOT_ID = 4
    PARMAS_ERROR = 5

    def __getattribute__(self,name) :
        if Status.__dict__.has_key(name) :
            return Status.__dict__[name]
        else :
            return None

    def __getitem__(self,name) :
        return Status().__getattribute__(name)
    
    def getReason(self, code,error=None):
        if error==None:
            return status_collection[code]
        else:
            return 'Info:%s,Error:%s'%(
                status_collection[code],
                error
            )

