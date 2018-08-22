from .Base import Base


class Cls2Teacher(Base):
    num = 0

    def __init__(self, owner_teacher, owner_class):
        Cls2Teacher.num += 1
        self.id = Cls2Teacher.num
        self.owner_teacher = owner_teacher
        self.owner_class = owner_class

    def __str__(self):
        return '(关联）%s with %s' % (self.owner_teacher, self.owner_class)
