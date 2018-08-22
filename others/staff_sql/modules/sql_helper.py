import pymysql
from conf import setting


class SqlHelper(object):
    def __init__(self):
        self.conn = pymysql.connect(**setting.conn_dict)
        self.cursor = self.conn.cursor()

    def execute(self, sql):
        try:
            res = self.cursor.execute(sql)
            if not res:
                print('没有任何数据')
                return
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            print('语句格式错误: %s' % e)

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    s = SqlHelper()
    s.execute('love')
