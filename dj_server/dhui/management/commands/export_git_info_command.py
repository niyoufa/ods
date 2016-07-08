#coding=utf-8

import datetime, logging, sys, pdb

from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option

import ods.clients.github3_client as github3_client
import ods.clients.mongodb_client as mongodb_client
import MySQLdb as mysql_client

InfoLogger = logging.getLogger("dhui_commands")
ErrorLogger = logging.getLogger("dhui_commands_error")

class Command(BaseCommand):
    help = "export git repository info"

    def handle(self, *args, **options):
        niyoufa = github3_client.Github3Client()
        repo_name = "program_document"
        repo_info = niyoufa.get_repo_info_tree(repo_name)
        coll = mongodb_client.get_coll("repository")
        repository = coll.find_one({"name":repo_name})
        if repository :
            repository["repo_info"] = repo_info
            repository["alter_time"] = str(datetime.datetime.now())\
            .split(".")[0]
        else :
            repository = dict(
                name = repo_name,
                repo_info = repo_info,
                create_time = str(datetime.datetime.now())\
            .split(".")[0],
                alter_time = "",
            )
        coll.save(repository)

        repo_files = niyoufa.get_repo_files(repo_name)
        coll = mongodb_client.get_coll("files")
        file_categs = repo_files.keys()
        for file_categ in file_categs:
            link = coll.find_one({"categ":file_categ})
            if link :
               link["files"] =  repo_files[file_categ]
               link["alter_time"] = str(datetime.datetime.now())\
                .split(".")[0]
            else :
                link = {}
                link["categ"] = file_categ
                link["files"] =  repo_files[file_categ]
                link["create_time"] = str(datetime.datetime.now())\
                .split(".")[0]
                link["alter_time"] = ""
            coll.save(link)
