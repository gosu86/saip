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
    
        ra = model.Rol()
        ra.rol_name = u'Administradores'
        ra.name = u'Administradores del sistema'    
        model.DBSession.add(ra)
        
        ra.usuarios.append(u)
          
        rde = model.Rol()
        rde.rol_name = u'Desarrolladores'
        rde.name = u'Desarrolladores de Items'
        model.DBSession.add(rde)

        rco = model.Rol()
        rco.rol_name = u'Configuradores'
        rco.name = u'Configuradores de Items'
        model.DBSession.add(rco)
            
        ra = model.Rol()
        ra.rol_name = u'Administrador'
        ra.name = u'Administrador del sistema'    
        model.DBSession.add(ra)
        
        ra.usuarios.append(u)         
        
        permisos_administrar    = ["AdministrarUsuarios","AdministrarRoles","AdministrarPermisos","AdministrarProyectos","AdministrarTodo"]
        permisos_configurar     = ["ConfigurarFases","ConfigurarProyectos","ConfigurarTiposDeItem","ConfigurarLineasBase","ConfigurarTodo"]
        permisos_desarrollar_y_aprobar    = ["DesarrollarItems","AprobarItems"]
        
        for nombre_permiso in permisos_administrar:            
            p = model.Permiso()
            p.permiso_name = unicode(nombre_permiso)
            p.descripcion = unicode('Da el permiso para '+space_out_camel_case(nombre_permiso))
            p.roles.append(ra)   
            model.DBSession.add(p)

        r = model.Rol()
        r.rol_name = u'Lider'
        r.name = u'Lider de Proyecto'
        model.DBSession.add(r)
                 
        for nombre_permiso in permisos_configurar:            
            p = model.Permiso()
            p.permiso_name = unicode(nombre_permiso)
            p.descripcion = unicode('Da el permiso para '+space_out_camel_case(nombre_permiso))
            p.roles.append(r)
            p.roles.append(ra)   
            model.DBSession.add(p)

        rapde = model.Rol()
        rapde.rol_name = u'Aprob. y Des.'
        rapde.name = u'Aprobador y Desarrollador de Items'
        model.DBSession.add(rapde)

        rap = model.Rol()
        rap.rol_name = u'Aprobador'
        rap.name = u'Aprobador de Items'
        model.DBSession.add(rap)
        
        rde = model.Rol()
        rde.rol_name = u'Desarrollador'
        rde.name = u'Desarrollador de Items'
        model.DBSession.add(rde)
        c=0
        for nombre_permiso in permisos_desarrollar_y_aprobar:            
            p = model.Permiso()
            p.permiso_name = unicode(nombre_permiso)
            p.descripcion = unicode('Da el permiso para '+space_out_camel_case(nombre_permiso))
            p.roles.append(rapde)
            p.roles.append(ra)
            if c==0:
                p.roles.append(rde)
            else:
                p.roles.append(rap)
            c=c+1
            model.DBSession.add(p)
        model.DBSession.flush()
        
        p               =   model.Proyecto()
        p.name          =   u"El proyecto"
        p.descripcion   =   u"Este es un proyecto de prueba"
        p.empresa       =   u"La empresa S.A."
        p.lider_id      =   u.id   
        model.DBSession.add(p)        
        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        print 'Warning, there was a problem adding your auth data, it may have already been added:'
        import traceback
        print traceback.format_exc()
        transaction.abort()
        print 'Continuing with bootstrapping...'


    # <websetup.bootstrap.after.auth>
