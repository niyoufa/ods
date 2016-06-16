#coding=utf-8

import xlsxwriter
import datetime
import pdb

import ods.settings as settings

class Xlsx_Reporter(object):
    """
        xlsx报表生成器
        author : niyoufa
        date : 2016-06-16
        refer : xlsxwriter
    """

    def __get_workbook_name(self,*args,**options):
        return options.get("filename",settings.REPORT_PATH + str(datetime.datetime.now()).replace("-","_").\
        replace(" ","_").replace(":","_").replace(".","_")) + ".xlsx"

    def __create_workbook(self,filename,*args,**options):
        return xlsxwriter.Workbook(filename)

    def __create_worksheets(self,workbook,worksheet_names):
        worksheet_dict = {}
        if type(worksheet_names) != type([]):
            raise Exception("param error :work sheet names should be a list")
        elif len(worksheet_names) == 0:
            worksheet_names.append("Sheet1")
        else:
            pass
        for name in worksheet_names :
            worksheet = workbook.add_worksheet(name)
            worksheet_dict[name]= worksheet

        return worksheet_dict

    def __init__(self,*args,**options):
        self.filename = self.__get_workbook_name(*args,**options)
        self.worksheet_names = options.get("worksheet_names",[])
        self.workbook = self.__create_workbook(self.filename)
        self.workbook.worksheet_names = self.worksheet_names
        self.worksheet_dict = self.__create_worksheets(self.workbook,self.workbook.worksheet_names)

    def get_worksheet(self, worksheet_name=None):
        if worksheet_name == None :
            return self.worksheet_dict.values()[0]
        worksheet = self.worksheet_dict.get(worksheet_name, None)
        return worksheet

    def get_worksheets(self,worksheet_names):
        return [self.get_worksheet(name) for name in worksheet_names]

    def get_all_worksheet(self):
        worksheet_names = self.worksheet_names
        worksheets = self.get_worksheets(worksheet_names)
        return worksheets

    def close(self):
        self.workbook.close()

    # 生成xlsx报表
    def report(self):
        pass

    # 生成发货单xlsx报表
    def report_invoice(self):
        pass

if __name__ == "__main__":
    pass
    xlsx_reporter = Xlsx_Reporter()
    print xlsx_reporter
    xlsx_reporter.close()