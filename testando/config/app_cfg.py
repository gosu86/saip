# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in testando.

This file complements development/deployment.ini.

Please note that **all the argument values are strings**. If you want to
convert them into boolean, for example, you should use the
:func:`paste.deploy.converters.asbool` function, as in::
    
    from paste.deploy.converters import asbool
    setting = asbool(global_conf.get('the_setting'))
 
"""
from routes import Mapper
from tg.configuration import AppConfig, config
import logging
import testando
from testando import model
from testando.lib import app_globals, helpers 

def setup_routes(self):
    """Setup the default TG2 routes

    Override this and set up your own routes maps if you want to use routes.
    """
    map = Mapper(directory=config['pylons.paths']['controllers'],
                always_scan=config['debug'])
    # Setup a default route for the root of object dispatch
    map.connect('/proyectos/', controller='proyectoscontroller', action='index')
    map.connect('*url', controller='root', action='routes_placeholder')

    config['routes.map'] = map


base_config = AppConfig()
base_config.renderers = []
base_config.package = testando

#Enable json in expose
base_config.renderers.append('json')
#Set the default renderer
base_config.default_renderer = 'genshi'
base_config.renderers.append('genshi')
# if you want raw speed and have installed chameleon.genshi
# you should try to use this renderer instead.
# warning: for the moment chameleon does not handle i18n translations
#base_config.renderers.append('chameleon_genshi')

#Configure the base SQLALchemy Setup
base_config.use_sqlalchemy = True
base_config.model = testando.model
base_config.DBSession = testando.model.DBSession

# Configure the authentication backend

# YOU MUST CHANGE THIS VALUE IN PRODUCTION TO SECURE YOUR APP 
base_config.sa_auth.cookie_secret = "F*#%You!..YouChangeYourSelf!" 

base_config.auth_backend = 'sqlalchemy'
base_config.sa_auth.dbsession = model.DBSession
# what is the class you want to use to search for users in the database
base_config.sa_auth.user_class = model.Usuario
base_config.sa_auth.translations.users = 'usuarios'
base_config.sa_auth.translations.user_name = 'usuario_name'
base_config.sa_auth.translations.validate_password = 'validar_password'
# what is the class you want to use to search for groups in the database
base_config.sa_auth.group_class = model.Rol
base_config.sa_auth.translations.groups = 'roles'
base_config.sa_auth.translations.group_name = 'rol_name'
# what is the class you want to use to search for permissions in the database
base_config.sa_auth.permission_class = model.Permiso
base_config.sa_auth.translations.permissions = 'permisos'
base_config.sa_auth.translations.permission_name = 'permiso_name'
# override this if you would like to provide a different who plugin for
# managing login and logout of your application
base_config.sa_auth.form_plugin = None

# override this if you are using a different charset for the login form
base_config.sa_auth.charset = 'utf-8'

# You may optionally define a page where you want users to be redirected to
# on login:
base_config.sa_auth.post_login_url = '/post_login'

# You may optionally define a page where you want users to be redirected to
# on logout:
base_config.sa_auth.post_logout_url = '/post_logout'
