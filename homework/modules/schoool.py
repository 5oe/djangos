from .Base import Base


class School(Base):
    def __init__(self, sname, sarea):
        self.sname = sname
        self.sarea = sarea

    def __str__(self):
        return '（学校）%s%s校区' % (self.sname, self.sarea)
