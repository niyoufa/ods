#coding=utf-8

import datetime, logging, sys, pdb

from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option

import ods.dhui.dhui_order as do
import ods.dhui.dhui_order_line as dol
import ods.dhui.dhui_product_template as dpt
import ods.clients.mongodb_client as mongodb_client
import ods.clients.xmlrpc_client as xmlrpc_client
import ods.utils as utils
import ods.dhui.dhui_invoice as di

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

class Command(BaseCommand):
    help = "供应商发货单发货明细"

    def handle(self, *args, **options):
        utils.create_order_invoice(do=do,dol=dol,dpt=dpt,di=di,mongodb_client=mongodb_client,xmlrpc_client=xmlrpc_client)
