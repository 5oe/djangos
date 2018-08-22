from modules.sql_helper import SqlHelper

class LogicHandler(object):
    def __init__(self):
        self.sql_helper = SqlHelper()
        self.show_menu()

    def show_menu(self):
        while True:
            # print('1.查询操作')
            # print('2.插入新数据')
            # print('3.修改旧数据')
            sql = input('请输入sql查询：')
            data= self.sql_helper.execute(sql)
            if data:
                for i in data:
                    print(i)
