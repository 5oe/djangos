import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import modules

if __name__ == '__main__':
    form_data = {
        'first': 'true',
        'pn': '1',  # 初始页为1
        'kd': 'python',
    }

    param_data = {
        'city': '广州',
        'needAddtionalResult': 'false',
    }

    modules.run(
        url='https://www.lagou.com/jobs/positionAjax.json',
        param_data=param_data,
        form_data=form_data
    )
