#coding=utf-8

import pdb
import sys
sys.path.append("..")
import odoo_dock
import ods.clients.xmlrpc_client as xmlrpc_client
import ods.clients.mongodb_client as mongodb_client
import ods.utils as utils
import ods.settings as settings

def init_stock_info(*args,**options):
    coll = mongodb_client.get_coll("DHUI_Product")

    print "start init product good ..."

    good_list = coll.find()[0:1]
    for good in good_list:
        goods_name = good["goods_name"]
        pt_xmlrpcclient = xc.get_xmlrpcclient("ProductTemplate")
        pp_xmlrpcclient = xc.get_xmlrpcclient("Product")
        product_id, product_template_id = utils.get_product_id(pt_xmlrpcclient, pp_xmlrpcclient, good)
        if not product_id:
            continue
        else:
            pdb.set_trace()

            # xmlrpcclient = xc.get_xmlrpcclient("StockQuant")
            # stock_quant_obj = dict(
            #     product_id = product_id,
            #     qty = 0.0,
            #     location_id = 12,
            # )
            # utils.load_obj(xmlrpcclient,stock_quant_obj)
            #
            # xmlrpcclient = xc.get_xmlrpcclient("StockInventory")
            # stock_inventory_obj = dict(
            #     product_id = product_id,
            #     location_id = 12,
            #     name = 'INV: '+'不二家牛乳糖拉链罐装30g',
            #     filter = "product",
            #     state = 'done'
            # )
            # stock_inventory_obj_id = utils.load_obj(xmlrpcclient, stock_inventory_obj)
            #
            # xmlrpcclient = xc.get_xmlrpcclient("StockInventoryLine")
            # stock_inventory_line_obj = dict(
            #     product_id=product_id,
            #     product_name=goods_name,
            #     product_qty=0.0,
            #     location_id=12,
            #     inventory_id = stock_inventory_obj_id,
            #     company_id = 1,
            # )
            # utils.load_obj(xmlrpcclient, stock_inventory_line_obj)
            #
            # xmlrpcclient = xc.get_xmlrpcclient("StockMove")
            # stock_move_obj = dict(
            #     product_id = product_id,
            #     product_uom_qty = 1.0,
            #     state = "done",
            #     product_uom = 1,
            #     location_id = 12,
            #     location_dest_id = 5,
            #     name = 'INV:INV: '+'不二家牛乳糖拉链罐装30g',
            #     product_uos = 1,
            #     inventory_id = stock_inventory_obj_id,
            # )
            # utils.load_obj(xmlrpcclient,stock_move_obj)

            xmlrpcclient = xc.get_xmlrpcclient("StockChangeProductQty")
            stock_chane_product_qty_obj = dict(
                product_id=product_id,
                new_quantity=1,
                location_id=12,
                lot_id=False,
            )
            utils.load_obj(xmlrpcclient, stock_chane_product_qty_obj)


if __name__ == "__main__":
    init_stock_info()