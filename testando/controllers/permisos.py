from tg             import expose
from tgext.crud     import CrudRestController
from repoze.what.predicates import All,not_anonymous,has_any_permission

from testando.model	            	import DBSession
from testando.model.auth        	import Permiso

__all__ = ['PermisosController']
class PermisosController(CrudRestController):
	allow_only = All(not_anonymous(msg='Acceso denegado. Ud. no se ha loqueado!'),
					 has_any_permission('AdministrarTodo',
										'AdministrarPermisos',
										msg='Solo usuarios con los permisos "AdministrarTodo" y/o "AdministrarPermisos" acceder a esta seccion!'))	
	model 		= 	Permiso

	@expose('testando.templates.administrar.permisos.index')
	def get_all(self):
		return dict(page="Administrar")
