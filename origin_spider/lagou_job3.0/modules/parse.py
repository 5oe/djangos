

class Parse(object):
    def __init__(self, response_dict):
        self.response_dict = response_dict

    @property
    def page_num(self):
        '''
        解析并计算页面数量
        :return: 页面数量
        '''
        total_count = self.response_dict['content']['positionResult']['totalCount']  # 职位总数量
        result_size = self.response_dict['content']['positionResult']['resultSize']  # 每一页显示的数量
        page_count = int(total_count) // int(result_size) + 1  # 页面数量
        return page_count

    def parse_content(self):
        # return [row_dict for row_dict in \
        #         self.response_dict['content']['positionResult']['result']]

        ret = []
        for row in self.response_dict['content']['positionResult']['result']:
            tmp_dict = dict()
            tmp_dict['companyName'] = row['companyFullName']
            tmp_dict['companyDistrict'] = row['district']
            tmp_dict['companyLabel'] = row['companyLabelList']
            tmp_dict['companySize'] = row['companySize']
            tmp_dict['companyStage'] = row['financeStage']
            tmp_dict['companyType'] = row['industryField']
            tmp_dict['positionName'] = row['positionName']
            tmp_dict['positionType'] = row['firstType']
            tmp_dict['positionEducation'] = row['education']
            tmp_dict['positionAdvantage'] = row['positionAdvantage']
            tmp_dict['positionSalary'] = row['salary']
            tmp_dict['positionWorkYear'] = row['workYear']
            ret.append(tmp_dict)
        return ret


