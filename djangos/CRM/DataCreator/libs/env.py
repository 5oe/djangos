def init():
    import os, django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRM.settings")  # project_name 项目名称
    django.setup()
