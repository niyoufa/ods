#coding=utf-8

from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option
import datetime,logging

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

class Command(BaseCommand):
    help = "供应商发货单发货明细"

    def handle(self, *args, **options):
        pass