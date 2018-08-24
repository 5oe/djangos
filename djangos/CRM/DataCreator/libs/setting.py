from DataCreator.conf import setting


def get_setting(setting_name):
    if hasattr(setting, setting_name):
        return getattr(setting, setting_name)
    else:
        return None
