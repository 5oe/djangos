from .Base import Base


class Subject(Base):
    def __init__(self, sname, scyc_days, sprice, owner_school):
        self.sname = sname
        self.scyc_days = scyc_days
        self.sprice = sprice
        self.owner_school = owner_school

    def __str__(self):
        return '（课程）设在%s的%s' % (self.owner_school, self.sname)
