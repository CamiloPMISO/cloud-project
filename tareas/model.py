import db
from sqlalchemy import Column, Integer, String, Float


class Tarea(db.Base):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True)
    fileName = Column(String, nullable=False)
    originalFormat = Column(String, nullable=False)
    newFormat = Column(String, nullable=False)
    timeStamp = Column(String, nullable=False)
    lastUpdate = Column(String, nullable=False)
    status = Column(String, nullable=False)
    usuario = Column(Integer, nullable=False)

    def __init__(self, fileName, originalFormat, newFormat, timeStamp, status, usuario):
        self.fileName = fileName
        self.originalFormat = originalFormat
        self.newFormat = newFormat
        self.timeStamp = timeStamp
        self.status = status
        self.usuario = usuario

    def __repr__(self):
        return f'Tarea({self.fileName})'
    def __str__(self):
        return self.fileName


