import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
DB_DIR = os.path.join(BASE_DIR, 'db')

from modules.student import Student
ADMIN_INFO = [('admin', 'admin')]
login_info = {'uaccount': None, 'type': '', 'isLogin': False}
