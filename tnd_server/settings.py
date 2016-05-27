#coding=utf-8
import os , sys , pdb
import platform

sys.path.append(os.path.dirname(os.getcwd()))
import swallow

BASE_DIR = os.path.dirname(swallow.__file__)

SERVER_HOST = "localhost"
SERVER_PORT = 8888

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017

HOST = "localhost"
PORT = 27018