from .Base import Base


class Class(Base):
    def __init__(self, cname, owner_subject, owner_school):
        self.cname = cname
        self.owner_subject = owner_subject
        self.owner_school = owner_school

    def __str__(self):
        return '(课程)位于%s的%s ' % (self.owner_school, self.cname)
