#coding=utf-8

import datetime, logging, sys, pdb

from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option

import ods.clients.mongodb_client as mongodb_client
import MySQLdb as mysql_client

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

class Command(BaseCommand):
    help = "export git repository info"

    def handle(self, *args, **options):
        coll = mongodb_client.get_coll("links")
        links = []
        link_obj_list = coll.find({},{"files":1})
        for link_obj in link_obj_list:
            links.extend(link_obj["files"])

        #export to mysql
        db = mysql_client.connect("localhost","root","dhui123","demosite")
        cr = db.cursor()
        cr.execute("delete from demosite_links")
        for link in links :
            name = link['name'].encode("utf-8")
            download_url = link["download_url"].encode("utf-8")
            curr_time = str(datetime.datetime.now()).split(".")[0]\
            .encode("utf-8")
            sql = "insert into demosite_links\
            (title,url,time) values(\'%s\',\'%s\',\'%s\')"\
                %(name,download_url,curr_time)
            cr.execute(sql)
        db.commit()
        cr.execute("select * from demosite_links")
        data = cr.fetchall()
        pdb.set_trace()
        print data
        db.close()