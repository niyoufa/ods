# ods
odoo dock system

odoo开源ERP系统对接系统

1. 系统架构
ods包括三个逻辑部分：
    ods.clients ： 操作odoo数据对象模块和操作mongodb数据模块,
    ods.dj_server: 命令执行系统，基于django的BaseCommand ,
    ods.tnd_server: API服务系统，给予tornado的后端服务接口,


2. ods.clients

ods.clients.xmlrpc_client    : 提供操作odoo数据对象的接口
ods.clients.mongodb_client   : 提供操作mongodb数据对象接口

3. ods.dhui

结合业务逻辑和ods.clients.xmlrpc_client ， 进一步封装了提供操作odoo数据对象的接口

4. ods.dj_server

使用方法 ：
在 dj_server目录下执行：python manage.py
打印出 dhui命令列表 ：
[dhui]
    dhui_init_partner_info_command ： 初始化供应商信息
    dhui_init_product_data_command ： 初始化商品信息
    dhui_sale_order_command ： 导入订单数据
    init_schema ： 初始化psql表格建表
    partner_order_deliver_details ： 生成发货信息明细

5. ods.tnd_server

提供给客户端app数据接口

相关认证命令：
sudo ssh admin@120.26.226.63 -i id_rsa
su odoo -s /bin/bash
nohup mongod -f /etc/local_mongdb.conf &
mongo --host 120.26.226.63 --port 27018

ip : 120.26.226.63
账号密码 : root Dhui12345

SERVER_MONGODB_USER = "viewer"
SERVER_MONGODB_PASS = "DhuiViewer2016"

查看日志
tail dj_server/logs/dhui_commands.log | grep 2016-06-07



