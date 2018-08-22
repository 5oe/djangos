from .Base import Base


class ClassRecord(Base):
    def __init__(self, owner_teacher, owner_class, ctime):
        self.owner_teacher = owner_teacher
        self.owner_class = owner_class
        self.ctime = ctime
