from tg             import expose,redirect, validate,flash,tmpl_context
from tg.decorators  import override_template

from tgext.crud     import CrudRestController

from repoze.what.predicates import All,not_anonymous,has_any_permission

from testando.model             	import DBSession
from testando.model.proyecto        import Proyecto
from testando.model.auth        	import Usuario
from testando.model.fase        	import Fase
from testando.widgets.proyecto_w 	import proyecto_new_form,proyecto_edit_filler,proyecto_edit_form
from testando.widgets.myWidgets 	import hideMe

from formencode		import validators

import logging
__all__ = ['ProyectosController']
log = logging.getLogger(__name__)
class ProyectosController(CrudRestController):
	log.debug('<-- In to ProyectosController -->')
	allow_only = All(not_anonymous(msg='Acceso denegado. Ud. no se ha logueado!'),
					 has_any_permission('AdministrarTodo',
										'AdministrarProyectos',
										msg='Solo usuarios con los permisos "AdministrarTodo" y/o "AdministrarProyectos" acceder a esta seccion!'))	
	model		=	Proyecto
	new_form 	=	proyecto_new_form
	edit_filler	=	proyecto_edit_filler
	edit_form 	=	proyecto_edit_form

	template=''
	page=''
	@expose()
	def put(self, *args, **kw):
		"""update"""
		id=kw['name']
		log.debug('id: %s' %id )
		pks = self.provider.get_primary_fields(self.model)
		for i, pk in enumerate(pks):
			if pk not in kw and i < len(args):
				kw[pk] = args[i]
		d={'id':kw[pk]}
		p=DBSession.query(Proyecto).filter_by(**d).first()
		log.debug('proyecto.name: %s' %p.name )
		p.name=kw['name']
		p.empresa=kw['empresa']
		p.estado=kw['estado']
		p.descripcion=kw['descripcion']
		p.lider_id=int(kw['lider'])
		DBSession.flush()
		redirect('../' * len(pks))

	@expose('json')
	def usuarios(self):
		usuarios=DBSession.query(Usuario)
		names=''
		ids=''
		for u in usuarios:
			names=names+'"'+u.name+'"'+','
			ids=ids+str(u.id)+','
		names=names+'""'
		ids=ids+'""'
		return dict(names=names,ids=ids)

	@expose()
	def get_all(self,):
		override_template(self.get_all,self.template)		
		return dict(page=self.page)
			
	@validate(validators={"id":validators.Int()})
	@expose('json')
	def post_delete(self,**kw):
		id = kw['id']
		log.debug("Inside post_fetch: id == %s" % (id))
		if (id != None):
			d = {'id':id}
			proyecto = DBSession.query(Proyecto).filter_by(**d).first()
			nombre=proyecto.name
			if (proyecto.estado != 'Iniciado'):
				DBSession.delete(proyecto)
				DBSession.flush()
				msg="El proyecto se ha eliminado con exito!."
				type="succes"
			else:
				msg="El proyecto esta Iniciado! No se puede eliminar."
				type="error"
		return dict(msg=msg,nombre=nombre,type=type)			
				
	@expose()
	def get_one(self, *args, **kw):
		redirect('../')
		
	@validate(validators={"page":validators.Int(), "rp":validators.Int()})
	@expose('json')
	def lista_de_proyectos(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
		try:
			offset = (int(page)-1) * int(rp)
			if (query):
				d = {qtype:query}
				proyectos = DBSession.query(Proyecto).filter_by(**d)
			else:
				proyectos = DBSession.query(Proyecto)
			
			total = proyectos.count()
			column = getattr(Proyecto, sortname)
			proyectos = proyectos.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)
			for p in proyectos:
				log.debug("Lider == %s" % (p.lider.name))
			
			rows = [{'id'  : proyecto.id,
					'cell': [proyecto.id,
							proyecto.name,
							proyecto.lider.name,
							proyecto.descripcion,
							proyecto.estado,
							(', '.join([f.name for f in proyecto.fases]))]} for proyecto in proyectos]
			result = dict(page=page, total=total, rows=rows)
		except:
			result = dict() 
		return result		