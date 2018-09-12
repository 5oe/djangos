import importlib
from django.conf import settings
from django.db import models


class AcquireForModel(object):
    def __init__(self):
        self.model_cls = {}
        self.__init()

    def __init(self):
        model_to_cls = {}
        for app in settings.INSTALLED_APPS:
            if not app.startswith('django.contrib.'):
                model_to_cls[app] = []
                m = importlib.import_module(app + '.models')
                self.add_models_class(m, model_to_cls[app])
        self.model_cls = model_to_cls

    @staticmethod
    def add_models_class(model, l):
        for obj_str in dir(model):
            obj = getattr(model, obj_str)
            try:
                if issubclass(obj, models.Model):
                    l.append(obj)
            except:
                pass
