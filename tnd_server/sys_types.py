# -*- coding: utf-8 -*-

def enum(**kwargs):
    enums = {}
    attrs = {}
    keys = {}

    for key, (value, name) in kwargs.items():
        enums[value] = name
        attrs[key] = value
        keys[key] = value

    #声明为类方法，可以取得类属性
    @classmethod
    def tuples(cls):
        return cls.ENUMS.items()

    attrs['ENUMS'] = enums
    attrs['KEYS'] = keys
    attrs['tuples'] = tuples

    #动态生成Enum类，类属性动态变化
    return type('Enum', (object, ), attrs)

#Mongodb Collection Type Define
CollectionType = enum(
    UserAddress = (0,u"用户地址表") ,
)

