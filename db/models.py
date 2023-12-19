from db.database import Base
from sqlalchemy import Boolean, Column,Date,Time,DateTime, Table
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


tag_task_association = Table(
    'tag_task_association',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id')),
    Column('task_id', Integer, ForeignKey('tasks.id'))
)

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class DbTask(Base):
    __tablename__='tasks'
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String,index=True)
    description=Column(String)
    task_status=Column(String)
    priority=Column(String)
    flag=Column(Boolean)
    date=Column(Date)
    time=Column(Time)
    folder_id=Column(Integer, ForeignKey("folders.id", ondelete='CASCADE'))
    folder=relationship("DbFolder", back_populates="tasks", foreign_keys=[folder_id])
    user_id=Column(Integer, ForeignKey("users.id", ondelete='CASCADE')) 
    user = relationship("DbUser", back_populates='items',foreign_keys=[user_id])
<<<<<<< Updated upstream
=======
    image_url = Column(String, nullable=True)
    image_url_type = Column(String, nullable=True)
    tags = relationship("Tag", secondary=tag_task_association, back_populates="tasks")
>>>>>>> Stashed changes

class DbFolder(Base):
    __tablename__='folders'
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String,index=True)
    tasks = relationship("DbTask", back_populates="folder", foreign_keys=[DbTask.folder_id])
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('DbUser', back_populates='folders')

class DbUser(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String )
  email = Column(String)
  password = Column(String)
  items = relationship('DbTask', back_populates='user', foreign_keys=[DbTask.user_id])
<<<<<<< Updated upstream
  folders = relationship('DbFolder', back_populates='user', cascade='all, delete-orphan')
=======





>>>>>>> Stashed changes
