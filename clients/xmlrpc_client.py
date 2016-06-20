#coding=utf-8

import xmlrpclib,pdb
import ods.settings as settings

class DB_CONST :
    DB_NAME = "db_name"
    TABLE_NAME = "table_name"
    TABLE_TYPE = "table_type"

class TABLES :

    # odoo table 配置
    __TABLES = dict(
        ProductTemplate = dict(table_name="product.template",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        IrProperty  = dict(table_name="ir.property",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        StockWarehouseOrderpoint = dict(table_name="stock.warehouse.orderpoint",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        ProductSupplierInfo = dict(table_name="product.supplierinfo",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        Product = dict(table_name="product.product",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        SaleOrder = dict(table_name="sale.order",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        SaleOrderLine = dict(table_name="sale.order.line",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        SaleOrderAddress = dict(table_name="sale.order.address",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        PurchaseOrder = dict(table_name="purchase.order",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        PurchaseOrderLine = dict(table_name="purchase.order.line",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        StockQuant = dict(table_name="stock.quant",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        StockMove = dict(table_name="stock.move",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        StockInventory = dict(table_name="stock.inventory",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        StockChangeProductQty = dict(table_name="stock.change.product.qty",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        StockInventoryLine = dict(table_name="stock.inventory.line",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        ResPartner = dict(table_name="res.partner",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        DhuiUser = dict(table_name="dhui.user",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        DhuiPurchaseUserLine = dict(table_name="dhui.purchase.user.line",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        DhuiPurchase = dict(table_name="dhui.purchase",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        DhuiInvoice = dict(table_name="dhui.invoice",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        DhuiAddress = dict(table_name="dhui.address",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        DhuiShipping = dict(table_name="dhui.shipping",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        DhuiShippingAddress = dict(table_name="dhui.shipping.address",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        DhuiShippingKuaidi = dict(table_name="dhui.kuaidi",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        DhuiShippingKuaidiLastresult = dict(table_name="dhui.kuaidi.lastresult",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),

        DhuiShippingKuaidiLastresultLine = dict(table_name="dhui.kuaidi.lastresult.line",db_name=settings.DHUI_ODOO_DATABASE,table_type=None),
    )

    @classmethod
    def get_db_name(cls,table_name) :
        if cls.__TABLES.has_key(table_name):
            odoo_db_name = cls.__TABLES[table_name][DB_CONST.DB_NAME]
        else :
            odoo_db_name = ""
        return odoo_db_name

    @classmethod
    def get_table_name(cls,table_name) :
        if cls.__TABLES.has_key(table_name):
            odoo_table_name = cls.__TABLES[table_name][DB_CONST.TABLE_NAME]
        else :
            odoo_table_name = ""
        return odoo_table_name

class XmlRpcClient(object):

    def __init__(self,model,db,host=settings.ODOO_HOST,port=settings.ODOO_PORT,
        user=settings.ODOO_USER,password=settings.ODOO_PASS):
        self._model = model
        self._host = host
        self._port = port
        self._user = user
        self._pass = password
        self._root = 'http://%s:%d/xmlrpc/' % (host,port)
        self._db = db
        self._uid = xmlrpclib.ServerProxy(self._root + 'common').login(db,user,password)
        self._models = xmlrpclib.ServerProxy(self._root + 'object')

    def search(self,query_params,offset=0,limit=None):
        query_list = []
        for key in query_params :
            query_list.append([key,'=',query_params[key]])
        result = self._models.execute_kw(self._db, self._uid, self._pass,
        self._model, 'search',
        [query_list])
        return result

    def search_count(self,query_params):
        query_list = []
        for key in query_params :
            query_list.append([key,'=',query_params[key]])
        count = self._models.execute_kw(self._db, self._uid, self._pass,
        self._model, 'search_count', 
        [query_list])
        return count

    def read(self,query_params,*args):
        query_list = []
        if len(args) :
            extra_query_params = args[0]
            for key in extra_query_params:
                query_list.append([extra_query_params[key][0], extra_query_params[key][1], extra_query_params[key][2]])
        else :
            #不做处理
            pass
        for key in query_params:
            query_list.append([key, '=', query_params[key]])
        result = self._models.execute_kw(self._db, self._uid, self._pass,
        self._model, 'search_read',
        [query_list])
        return result

    def read_by_ids(self,query_params):
        id_list = query_params["id_list"]
        field_list = query_params["field_list"]
        result = self._models.execute_kw(self._db, self._uid, self._pass,
        self._model, 'read',
        [id_list], {'fields': field_list})
        return result

    def search_read(self,query_params,field_list):
        pass

    def create(self,obj):
        if type(obj) != type({}) :
            raise Exception("param error")
        else :
            try :
                id = self._models.execute_kw(self._db, self._uid,self._pass,
                self._model , 'create', [obj])
            except Exception,e:
                print e
                return
            print "create :%s\n"%id
            print obj
            print "\n"
            return id

    def batch_create(self,obj_list):
        if type(obj_list) != type([]) :
            raise Exception("param error")
        else:
            create_id_list = []
            for obj in obj_list :
                id = self._models.execute_kw(self._db, self._uid,self._pass,
                self._model , 'create', [obj])
                print "create success :%s\n"%id
                create_id_list.append(id)
        return create_id_list

    def update(self,obj_id,alter_params):
        self._models.execute_kw(self._db, self._uid,self._pass,
        self._model, 'write', [[obj_id], alter_params])
        print "update :%s\n"%obj_id
        print alter_params
        print "\n"

    def batch_update(self,obj_list):
        if type(obj_list) != type([]):
            raise Exception("param error")
        else:
            for obj in obj_list:
                obj_id = obj["id"]
                alter_params = obj["alter_params"]
                # self._models.execute_kw(self._db, self._uid, self._pass,
                # self._model, 'write', [[obj_id],alter_params])
                # print "update success :%s\n" % id
                self.update(obj_id,alter_params)

xmlrpcclient_dict = {}

def get_xmlrpcclient(table_name):
    if xmlrpcclient_dict.has_key(table_name):
        return xmlrpcclient_dict[table_name]
    else :
        model = TABLES.get_table_name(table_name)
        db = TABLES.get_db_name(table_name)
        xmlrpcclient = XmlRpcClient(model,db)
        xmlrpcclient_dict[table_name] = xmlrpcclient
        return xmlrpcclient

    





    






