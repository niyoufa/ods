# -*- coding: utf-8 -*-
from django.conf import settings
import re,time

def list_first_item(value):
    try:
        if not hasattr(value[0], '__iter__'):
            return [value[0]]
        else:
            return value[0]
    except Exception:
        return None

def float_equals(a, b):
    return abs(a - b) <= 1e-6

def uid(class_name):
    #将大写字母换成小写并在字母前加前缀_
    return re.sub(r'([A-Z])', r'_\1', class_name).lower()[1:]

#根据卡号返回消费类型,1:普通银行卡,2:加油卡,3:信用卡,1000:现金
def getPaymentTypeByCard(card,card_fromat=None):
    if card_fromat!=None:
        reobj = re.compile(card_fromat)
        result = reobj.match(card)

        #加油卡
        if result:
            return 2

    #银行卡号最多为19位
    if len(card)>19:
        return 1000

    #银行卡至少为16位,信用卡至少为14位
    if len(card)>=14:

        #前六位为银行卡的BIN
        front=int(card[:6])

        #信用卡BIN分配如下:
        #威士卡（VISA）:400000—499999;万事达卡（MasterCard）:510000—559999;
        #运通卡（American Express）:340000—349999，370000—379999;
        #大来卡（DinersClub）:300000—305999，309500—309599,360000—369999，380000—399999;
        #JCB卡（JCB）:352800—358999
        if (front>=300000 and front<=305999) or (front>=309500 and front<=305999) or \
            (front>=360000 and front<=369999) or (front>=380000 and front<=399999) or \
            (front>=352800 and front<=358999) or (front>=340000 and front<=349999) or \
            (front>=370000 and front<=379999) or (front>=510000 and front<=559999) or \
            (front>=400000 and front<=499999):
            return 3

        else:
            if len(card)>=16:
                card_front=card[:1]
                #普通银行卡以6,9开头,多数为6
                if card_front=='6' or card_front=='9':
                    return 1
                else:
                    return 1000

    #现金
    return 1000

#序列化交易编号
def compute_trans_id(data_time,shard_id,site_id,gun_id,money) :

    # 交易时间,32位
    data_time=long(int(data_time))
    data_time=data_time<<32

    #服务器编号，6位，最多64台
    shard_id=shard_id<<26

    #油站编号,10位，最多每个服务器上1024个
    site_id=site_id<<16

    #油枪号，7位，一个油站最多128个
    gun_id=gun_id<<9

    #金额 9位
    result=data_time+shard_id+site_id+gun_id+money
    
    return result

#反序列化交易编号
def deserialize_trans_id(long_trans_id):
    num=long(long_trans_id)
    # 获取高32位的时间
    time=int(num>>32)
    # 获取低32 位
    num=num & 0xFFFFFFFF
    shard_id=num>>26
    #取出低26位
    num=num & 0x3FFFFFF
    site_id=num>>16
    #取出低16位
    num=num & 0xFFFF
    gun_id=num>>9
    #获取金额
    money=num & 0x1FF
    return (time, shard_id, site_id, gun_id, money)
