def init(project_name):
    import os, django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" % project_name)  # project_name 项目名称
    django.setup()
