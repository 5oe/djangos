import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

conn_dict = dict(
    host='localhost',
    user='root',
    password='Yiyidongwang13@',
    database='my_pratice'
)

if __name__ == '__main__':
    print(conn_dict)
