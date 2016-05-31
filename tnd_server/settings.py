#coding=utf-8
import os , sys , pdb
import platform

sys.path.append(os.path.dirname(os.getcwd()))
import tnd_server

BASE_DIR = os.path.dirname(tnd_server.__file__)

SERVER_HOST = "localhost"
SERVER_PORT = 8889

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017

HOST = "localhost"
PORT = 27018