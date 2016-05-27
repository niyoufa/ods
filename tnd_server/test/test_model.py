#coding=utf-8

import sys , os

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

from user_address_demo import settings          
import model.user_address as UserAddress                

if __name__ == "__main__" :
    UserAddress.UserAddressModel.init_test_data()

