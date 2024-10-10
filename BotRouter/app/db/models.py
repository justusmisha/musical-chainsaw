from sqlalchemy import (
    Column, Integer, String, ForeignKey, JSON, BigInteger, LargeBinary
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class CommonEntity(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    prices = Column(JSON, default=None)
    min_age = Column(Integer, default=6)
    max_age = Column(Integer, default=17)
    schedule = Column(JSON, default={})
    contact_number = Column(String, default=None)


class Class(Base):
    __tablename__ = 'class'
    id = Column(Integer, primary_key=True)
    max_places = Column(Integer, default=None)
    left_places = Column(Integer, default=None)
    min_age = Column(Integer, default=None)
    max_age = Column(Integer, default=None)
    price = Column(BigInteger, default=None)
    schedule = Column(JSON, default={})
    class_number = Column(Integer, default=None)

    teachers = relationship("ClassTeacher", back_populates="class_")


class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    fio = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    file_path = Column(String, nullable=False)


    classes = relationship("ClassTeacher", back_populates="teacher")

    activities = relationship("SchoolActivity", back_populates="teacher", cascade="all, delete-orphan")
    clubs = relationship("SchoolClub", back_populates="teacher", cascade="all, delete-orphan")


class ClassTeacher(Base):
    __tablename__ = "classteacher"
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    class_id = Column(Integer, ForeignKey('class.id'))

    teacher = relationship("Teacher", back_populates="classes")
    class_ = relationship("Class", back_populates="teachers")


class SchoolActivity(CommonEntity):
    __tablename__ = 'schoolactivity'

    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    teacher = relationship("Teacher", back_populates="activities")


class SchoolClub(CommonEntity):
    __tablename__ = 'schoolclub'

    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    teacher = relationship("Teacher", back_populates="clubs")
