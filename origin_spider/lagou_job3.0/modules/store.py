import codecs
from conf import setting
from modules.log import logger


def init_store_file():
    title = '公司名称\t公司类型\t融资阶段\t标签\t公司规模\t公司所在地\t职位名称\t学历要求\t福利\t薪资\t工作经验\n'
    file = codecs.open('%s职位.xls' % setting.STORE_FILE_TITLE, 'w', 'utf-8')
    file.write(title)


def store(content):
    file = codecs.open('%s职位.xls' % setting.STORE_FILE_TITLE, 'a', 'utf-8')
    try:
        for row in content:
            line = str(row['companyName']) + '\t' + str(row['companyType']) + '\t' + str(row['companyStage']) + '\t' + \
                   str(row['companyLabel']) + '\t' + str(row['companySize']) + '\t' + str(
                row['companyDistrict']) + '\t' + \
                   str(row['positionName']) + '\t' + str(row['positionEducation']) + '\t' + str(
                row['positionAdvantage']) + '\t' + \
                   str(row['positionSalary']) + '\t' + str(row['positionWorkYear']) + '\n'
            file.write(line)
            logger.log(status=True, msg='记录成功%s' % str(row))
        file.close()
    except Exception as e:
        logger.log(status=False, msg='保存数据出错:%s' % str(e))
        print(e)
        return
