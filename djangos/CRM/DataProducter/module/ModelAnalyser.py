class ModelAnalyser(object):
    Char_fields = ['CharField']
    Number_fields = ['IntegerField', 'FloatField']
    Date_fields = []
    TextField = ''
    EmailField = ''

    def __init__(self, model_class):
        self.model_class = model_class


