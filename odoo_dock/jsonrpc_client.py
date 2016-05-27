#coding=utf-8
import jsonrpclib , pdb
import settings


# server proxy object
url = "http://%s:%s/jsonrpc" % (settings.HOST, settings.PORT)
server = jsonrpclib.Server(url)

# log in the given database
uid = server.call(service="common", method="login", args=[settings.DB, settings.USER, settings.PASS])

def invoke(model,method,*args):
    call_params = [settings.DB, uid, settings.PASS, model, method] + list(args)
    return server.call(service="object", method="execute", args=call_params)

def insert_model(model, *args):
    method = "create"
    return invoke(model,method,*args)

def search_model(model, *args):
    method = "search"
    return invoke(model,method,*args)

if __name__ == "__main__" :
    insert_data = {
        "name":"cars10",
        "create_uid": uid,
    }
    # print insert_model('academy.products', insert_data)

    search_data = [['name', '=', "cars10"],]
    limit = {"offset":0,"limit":10}
    print search_model('academy.products',search_data,limit)
