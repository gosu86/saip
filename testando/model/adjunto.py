from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, LargeBinary
from testando.model import DeclarativeBase


class Adjunto(DeclarativeBase):
    __tablename__ = 'adjuntos'
 
    id      =   Column(Integer, primary_key=True)
    
    name    =   Column(Unicode(150), nullable=False) 
    
    filecontent = Column(LargeBinary)

    item_id =   Column(Integer, ForeignKey('items.id'))



    