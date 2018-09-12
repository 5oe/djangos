class ForeignModelNullException(Exception):
    '''
    Custom exception types
    '''

    def __init__(self, related_model, column):
        err = '外键关联模型<{0}>的值列表为空,关联字段是{1}'. \
            format(related_model._meta.label, column)
        Exception.__init__(self, err)
        self.related_model = related_model
        self.column = column
