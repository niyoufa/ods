#coding=utf-8

import bypy
by = bypy.ByPy(configdir="test", debug=1, verbose=1)

by.upload("test" + '/a.txt')