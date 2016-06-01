# ods
odoo dock system

odoo开源ERP系统对接系统

1. 系统架构
ods包括三个逻辑部分：
    ods.clients ： 操作odoo数据对象模块和操作mongodb数据模块，
    ods.dj_server: 命令执行系统，基于django的BaseCommand ,
    ods.tnd_server: API服务系统，给予tornado的后端服务接口，
