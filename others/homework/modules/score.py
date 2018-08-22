from .Base import Base


class Score(Base):
    def __init__(self, owner_subject, owner_student, stime, sgrade):
        self.owner_subject = owner_subject
        self.owner_student = owner_student
        self.stime = stime
        self.sgrade = sgrade

    def __str__(self):
        return '%s: %s的作业' % (self.stime, self.owner_student)
