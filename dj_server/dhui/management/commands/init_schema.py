#coding=utf-8

import sys,pdb
from django.core.management.base import BaseCommand
from django.conf import settings
sys.path.append(settings.ODS_PARENT_PATH)
from ods.dj_server.dj_server import models

class Command(BaseCommand):
    help = 'Initialize the SQL models of station schema'

    def handle(self, *args, **options):
        try:
            conn = models.dash_db_manager.dash_engines[0].connect()
            tables = [
                models.OrderPurchaseDetail,
            ]
            for table in tables:
                table = table.__table__
                if not models.dash_db_manager.dash_engines[0].dialect.has_table(conn, table):
                    table.create(conn)
            self.stdout.write('Successfully initialized SQL models of station schema')
        except Exception, e:
            print >> sys.stderr, "Exception: ", str(e)
        finally:
            conn.close()