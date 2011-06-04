# -*- coding: utf-8 -*-
"""Setup the testando application"""

import logging
from tg import config
from testando import model
import re
import transaction

def space_out_camel_case(s):
    """Adds spaces to a camel case string.  Failure to space out string returns the original string.
    >>> space_out_camel_case('DMLSServicesOtherBSTextLLC')
    'DMLS Services Other BS Text LLC'
    """

    return re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z]))', ' ', s)


def bootstrap(command, conf, vars):
    """Place any commands to setup testando here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        u = model.Usuario()
        u.usuario_name = u'admin'
        u.name = u'Administrador'
        u.email = u'administrador@saip.com'
        u.password = u'pass'
    
        model.DBSession.add(u)
    
        r = model.Rol()
        r.rol_name = u'Administrador'
        r.name = u'Rol Administrador del sistema'
    
        r.usuarios.append(u)
    
        model.DBSession.add(r)
        
        permisos = ["AdministrarUsuarios","AdministrarRoles","AdministrarPermisos","AdministrarFases","AdministrarProyectos","AdministrarTiposDeItem","AdministrarTodo"]
        for nombre_permiso in permisos:            
            p = model.Permiso()
            p.permiso_name = unicode(nombre_permiso)
            p.descripcion = unicode('Da el permiso para '+space_out_camel_case(nombre_permiso))
            p.roles.append(r)   
            model.DBSession.add(p)
    
        u1 = model.Usuario()
        u1.usuario_name = u'desarrollador'
        u1.name = u'Desarrollador'
        u1.email = u'desarrollador@saip.com'
        u1.password = u'dpass'
        
        model.DBSession.add(u1)
        
        #=======================================================================
        # r = model.Rol()
        # r.rol_name = u'usuario'
        # r.name = u'Rol usuario del sistema'
        # 
        # model.DBSession.add(r) 
        #=======================================================================
        
        
        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        print 'Warning, there was a problem adding your auth data, it may have already been added:'
        import traceback
        print traceback.format_exc()
        transaction.abort()
        print 'Continuing with bootstrapping...'


    # <websetup.bootstrap.after.auth>
