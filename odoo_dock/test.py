#coding=utf-8

import xmlrpclib
import settings
import pdb
import models as Model_Type
import xmlrpc_client

root = 'http://%s:%d/xmlrpc/' % (settings.HOST, settings.PORT)

uid = xmlrpclib.ServerProxy(root + 'common').login(settings.DB, settings.USER, settings.PASS)
print "Logged in as %s (uid: %d)" % (settings.USER, uid)

# Create a new note
models = xmlrpclib.ServerProxy(root + 'object')

def test_xmlrpc_read():
    model = 'academy.products'

    #search
    result = models.execute_kw(settings.DB, uid, settings.PASS,
    model, 'search',
    [[['name', '=', "cars10"],]],   
    {'offset': 0, 'limit': 5})
    print "search"
    print result

    # search_count
    result = models.execute_kw(settings.DB, uid, settings.PASS,
    model, 'search_count',
    [[['name', '=', "cars10"],]])
    print "search_count"
    print result

    # read
    ids = models.execute_kw(settings.DB, uid, settings.PASS,
    model, 'search',
    [[['name', '=', "cars10"],]],
    {'limit': 1})
    record = models.execute_kw(settings.DB, uid, settings.PASS,
    model, 'read', [ids])
    print ids

    # read
    result = models.execute_kw(settings.DB, uid, settings.PASS,
    model, 'read',
    [[6]], {'fields': ['id', 'name', 'write_date']})
    print result

    #fields_get
    result = models.execute_kw(settings.DB, uid, settings.PASS,
    model, 'fields_get',
    [], {'attributes': ['name', 'write_date']})
    print result

    #search_read
    result = models.execute_kw(settings.DB, uid, settings.PASS,
    model, 'search_read',
    [[['name', '=', "cars10"],]],
    {'fields': ['name', 'id', 'write_date'], 'limit': 5})
    print result

    # name_get
    models.execute_kw(db, uid, password, 'res.partner', 'name_get', [[id]])

def test_xmlrpc_write():
    model = 'academy.products'

    # create
    id = models.execute_kw(settings.DB, uid, settings.PASS,
    model , 'create', [{
    'name': "New Partner",
    }])
    print id

    # write
    result = models.execute_kw(settings.DB, uid, settings.PASS,
    model, 'write', [[6], {
    'name': "Newer partner"
    }])
    print result

def test_xmlrpc_delete():
    model = 'academy.products'

    result = models.execute_kw(settings.DB, uid, settings.PASS, model, 'unlink', [[1]])
    print result

#test
if __name__ == "__main__" :
    model = Model_Type.Collections.get_coll_name("ProductTemplate")
    xmlrpcclient = xmlrpc_client.XmlRpcClient(model)
    obj_list = [
        dict(
            name = "Product1"
        ),
        dict(
            name = "Product2"
        ),
        dict(
            name = "Product3"
        ),
        dict(
            name = "Product4"
        ),
        dict(
            name = "Product5"
        ),
    ]
    obj_id_list = xmlrpcclient.batch_create(obj_list)