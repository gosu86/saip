# -*- coding: utf-8 -*-
"""
Auth* related model.

This is where the models used by :mod:`repoze.who` and :mod:`repoze.what` are
defined.

It's perfectly fine to re-use this definition in the testando application,
though.

"""
import os
from datetime import datetime
import sys
try:
    from hashlib import sha1
except ImportError:
    sys.exit('ImportError: No module named hashlib\n'
             'If you are on python2.4 this library is not part of python. '
             'Please install it. Example: easy_install hashlib')
from tg import config
from testando.model.fase            import usuario_rol_fase_table
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, synonym,relationship
from sqlalchemy.sql import select, and_
from testando.model import DeclarativeBase, metadata, DBSession
#from testando.model.proyecto import Proyecto
__all__ = ['Usuario', 'Rol', 'Permiso']


#{ Association tables


# This is the association table for the many-to-many relationship between
# groups and permissions. This is required by repoze.what.
rol_permiso_table = Table('roles_permisos', metadata,
    Column('rol_id', Integer, ForeignKey('roles.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('permiso_id', Integer, ForeignKey('permisos.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)

# This is the association table for the many-to-many relationship between
# groups and members - this is, the memberships. It's required by repoze.what.
usuario_rol_table = Table('usuarios_roles', metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('rol_id', Integer, ForeignKey('roles.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)


#{ The auth* model itself


class Rol(DeclarativeBase):
    """
    Group definition for :mod:`repoze.what`.

    Only the ``group_name`` column is required by :mod:`repoze.what`.

    """

    __tablename__ = 'roles'

    #{ Columns

    id = Column(Integer, autoincrement=True, primary_key=True)

    rol_name = Column(Unicode(16), unique=True, nullable=False)

    name = Column(Unicode(255))

    fecha_creacion = Column(DateTime, default=datetime.now)

    #{ Relations

    usuarios = relation('Usuario', secondary=usuario_rol_table, backref='roles')

    #{ Special methods

    def __repr__(self):
        return ('<Rol: nombre=%s>' % self.rol_name).encode('utf-8')

    def __unicode__(self):
        return self.rol_name

    #}


# The 'info' argument we're passing to the email_address and password columns
# contain metadata that Rum (http://python-rum.org/) can use generate an
# admin interface for your models.
class Usuario(DeclarativeBase):
    """
    User definition.

    This is the user definition used by :mod:`repoze.who`, which requires at
    least the ``user_name`` column.

    """
    __tablename__ = 'usuarios'

    #{ Columns

    id = Column(Integer, autoincrement=True, primary_key=True)

    usuario_name = Column(Unicode(16), unique=True, nullable=False)

    email = Column(Unicode(255), unique=True, nullable=False,
                           info={'rum': {'field':'Email'}})

    name = Column(Unicode(255))

    _password = Column('password', Unicode(80),
                       info={'rum': {'field':'Password'}})

    fecha_creacion = Column(DateTime, default=datetime.now)
    
    apellido = Column(Unicode(50))

    estado =  Column(Unicode(20))
    
    mis_proyectos       = relationship("Proyecto", order_by="Proyecto.id", backref="lider")
    #{ Special methods

    def __repr__(self):
        return ('<Usuario: nombre=%r, email=%r, display=%r>' % (
                self.usuario_name, self.email, self.name)).encode('utf-8')

    def __unicode__(self):
        return self.name or self.usuario_name

    #{ Getters and setters

    @property
    def permisos(self):
        """Return a set with all permissions granted to the user."""
        perms = set()
        for g in self.roles:
            perms = perms | set(g.permisos)
        return perms

    @classmethod
    def por_email(cls, email):
        """Return the user object whose email address is ``email``."""
        return DBSession.query(cls).filter_by(email=email).first()

    @classmethod
    def por_usuario_nombre(cls, username):
        """Return the user object whose user name is ``username``."""
        return DBSession.query(cls).filter_by(usuario_name=username).first()

    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        # Make sure password is a str because we cannot hash unicode objects
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(password + salt.hexdigest())
        password = salt.hexdigest() + hash.hexdigest()
        # Make sure the hashed password is a unicode object at the end of the
        # process because SQLAlchemy _wants_ unicode objects for Unicode cols
        if not isinstance(password, unicode):
            password = password.decode('utf-8')
        self._password = password

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))

    #}

    def validar_password(self, password):
        """
        Check the password against existing credentials.

        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool

        """
        hash = sha1()
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        hash.update(password + str(self.password[:40]))
        return self.password[40:] == hash.hexdigest()

    def roles_select(self,selected=None):
            """
            Devuelve un select tag con los roles posibles en una fase.
            """
            selectINI='<select id="'+str(self.id)+'">'
            op1='<option value=1>Aprobador</option>'
            op2='<option value=2>Desarrollador</option>'
            op3='<option value=3>Aprobador y Desarrollador</option>'            
            if selected==1:
                #log.debug('1')
                op1='<option value=1 selected="true">Aprobador</option>'
            elif selected==2:
                #log.debug('2')
                op2='<option value=2 selected="true">Desarrollador</option>'
                
            elif selected==3:
                #log.debug('3')
                op3='<option value=3 selected="true":>Aprobador y Desarrollador</option>'

            selectFIN='</select>'
            select=selectINI+op1+op2+op3+selectFIN
            
            return select

           
    def get_rol(self,fid):
        """
        Devuelve un select tag con el rol del usuario seleccionado por defecto. en la fase en configuracion.
        """
        fid=int(fid)
        conn = config['pylons.app_globals'].sa_engine.connect()
        se=select([usuario_rol_fase_table.c.rol_id],and_(usuario_rol_fase_table.c.usuario_id==self.id, usuario_rol_fase_table.c.fases_id==fid))
        
        result=conn.execute(se)
        row=result.fetchone() 
        rol=int(row['rol_id'])

        conn.close()
        select_tag=self.roles_select(rol) 
        return select_tag




class Permiso(DeclarativeBase):
    """
    Permission definition for :mod:`repoze.what`.

    Only the ``permission_name`` column is required by :mod:`repoze.what`.

    """

    __tablename__ = 'permisos'

    #{ Columns

    id = Column(Integer, autoincrement=True, primary_key=True)

    permiso_name = Column(Unicode(63), unique=True, nullable=False)

    descripcion = Column(Unicode(255))

    #{ Relations

    roles = relation(Rol, secondary=rol_permiso_table,
                      backref='permisos')

    #{ Special methods

    def __repr__(self):
        return ('<Permiso: nombre=%r>' % self.permiso_name).encode('utf-8')

    def __unicode__(self):
        return self.permiso_name

    #}


#}
