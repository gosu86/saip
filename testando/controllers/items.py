from tgext.crud     import CrudRestController
from tg             import redirect, request,response
from tg.decorators  import override_template,validate,without_trailing_slash,expose
from tg.controllers import CUSTOM_CONTENT_TYPE

from tg.configuration import config
from sqlalchemy.sql import and_
from string import find
from testando.model                 import DBSession
from testando.model.item            import Item
from testando.model.tipoitem        import TipoItem
from testando.model.atributoextra   import AtributoExtra
from testando.model.adjunto         import Adjunto
from testando.model.fase            import Fase
from formencode                     import validators

import logging
import pygraphviz as pgv

log = logging.getLogger(__name__)
class ItemsController(CrudRestController):
    log.debug('<-- In to ProyectosItems -->')
        
    model = Item
    
    @expose('testando.templates.desarrollar.items.index')
    def get_all(self):
        override_template(self.get_all,self.template)    
        return dict(page=self.page)

    @without_trailing_slash
    @expose('testando.templates.desarrollar.items.new')
    def new(self, *args, **kw):
        
        referer=request.headers.get("Referer", "")
        log.debug("referer == %s" % (referer))
        log.debug('kw %s' %str(kw))
        tdiid=int(kw['tdiid'])
        tdi=DBSession.query(TipoItem).filter_by(id=tdiid).first()
        fase_id=tdi.fase_id
        fase_orden=tdi.fase.orden
        
        cant=len(DBSession.query(Item).filter(and_(Item.fase_id==fase_id,Item.tipo_item_id==tdi.id)).all())
        cod=str(tdi.codigo)
        cod= cod+'-'+str(cant)
        version=1
        
        tipo_item_id=tdi.id
        attr_extra=tdi.campos_extra
        posibles_antecesores=False
        if fase_orden > 1:
            posibles_antecesores=DBSession.query(Item).filter(and_(Item.fase_id==(fase_orden-1),Item.historico==False))
            posibles_antecesores=posibles_antecesores.filter(Item.linea_base.has(estado='Activa'))
            posibles_antecesores=posibles_antecesores.filter(Item.estado!='Eliminado')
            
        posibles_padres=DBSession.query(Item).filter(and_(Item.fase_id==fase_id,Item.historico==False,Item.estado!='Eliminado'))
        return dict(page="Desarrollar",
                    attr_extra=attr_extra,
                    fase_id=fase_id,
                    fase_orden=fase_orden,
                    tipo_item_id=tipo_item_id,
                    posibles_padres=posibles_padres,
                    posibles_antecesores=posibles_antecesores,
                    referer=referer,
                    title_nav='Desarrollo de fases',
                    codigo=cod,
                    version=version)
    
    @expose()
    def post(self, *args, **kw):
        log.debug('post -> kw = %s' %str(kw))
        
        fid=kw['fase_id']
               
        i=self.provider.create(self.model, params=kw)
        ti=i.tipo_item
        i.fase.estado='En Desarrollo'
        
        for ce in ti.campos_extra:
            ae                  =   AtributoExtra()
            ae.valor            =   kw[str(ce.name)]
            ae.item_id          =   i.id
            ae.campo_extra_id   =   ce.id            
            DBSession.add(ae)            
        DBSession.flush()
        i.historico_id=i.id
        DBSession.flush()  
        raise redirect('/desarrollar/desarrollo_de_fases/?fid='+fid)
    
    @validate(validators={"page":validators.Int(), "rp":validators.Int()})
    @expose('json')
    def lista_de_Items(self, page='1', rp='25', sortname='id', sortorder='asc', qtype=None, query=None):
        try:
            #____________________________________________
            # hacer esto para cada dato del tipo numerico
            if (qtype=="id"):
                id=int(query)
            #_____________________________________________
            
            offset = (int(page)-1) * int(rp)
            if (query):
                d = {qtype:query}
                items = DBSession.query(Item).filter_by(**d)
            else:
                items = DBSession.query(Item)
            
            total = items.count()
            column = getattr(Item, sortname)
            items = items.order_by(getattr(column,sortorder)()).offset(offset).limit(rp)    
            rows = [{'id'  : item.id,
                    'cell': [item.id, item.name, item.descripcion]} for item in items]
            result = dict(page=page, total=total, rows=rows)
        except:
            result = dict() 
        return result
    
    @expose('json')
    def post_delete(self,**kw):
        
        item = DBSession.query(Item).filter_by(id = int(kw['id'])).first()
        item.estado='Eliminado'
        DBSession.flush()

        msg="El item se ha eliminado."
        return dict(msg=msg)
    
    
    @expose('testando.templates.desarrollar.items.edit')
    def edit(self, *args, **kw):
        referer=request.headers.get("Referer", "")        
        log.debug("len(kw) %s" %len(kw))
        
        if find(referer,'configurar') >=0:
            page='Configurar'
            title_nav='Lista de items'
        else:
            page='Desarrollar'
            title_nav='Desarrollo de fases'
            
        
        pks = self.provider.get_primary_fields(self.model)
        kw = {}
        for i, pk in  enumerate(pks):
            kw[pk] = args[i]

        i=DBSession.query(Item).filter_by(id=int(kw[pk])).first()

        fase_id=i.fase_id
        fase_orden=i.fase.orden
        
        posibles_antecesores=False
        if fase_orden > 1:
            posibles_antecesores=DBSession.query(Item).filter(and_(Item.fase_id==(fase_orden-1),
                                                                   Item.historico==False,
                                                                   Item.estado!='Eliminado')).all()
            
        posibles_padres=DBSession.query(Item).filter(and_(Item.fase_id==fase_id,
                                                          Item.id!=i.id,
                                                          Item.historico==False,
                                                          Item.estado!='Eliminado')).all()

        for h in i.hijos:
            if h in posibles_padres:
                posibles_padres.remove(h)

        
        return dict(page=page,
                    posibles_padres=posibles_padres,
                    posibles_antecesores=posibles_antecesores,
                    referer=referer,
                    title_nav=title_nav,
                    item=i)
        
    def nueva_version(self,kw,adjunto_id=None):
        i                   =   DBSession.query(Item).filter_by(id=int(kw['itemid'])).first()
        i.historico         =   True
        
        item                =   Item()
        if kw.has_key('name'):
            item.name           =   kw['name']
        else:
            item.name           =   i.name        
        item.fase           =   i.fase
        item.codigo         =   i.codigo
        item.version        =   i.version+ 1
        item.tipo_item      =   i.tipo_item
        
        if kw.has_key('descripcion'):
            item.descripcion           =   kw['descripcion']
        else:
            item.descripcion           =   i.descripcion         

        if kw.has_key('complejidad'):
            item.complejidad           =   kw['complejidad']
        else:
            item.complejidad           =   i.complejidad
                    
        item.historico_id   =   i.historico_id
        
        if kw.has_key('atributos_extra'):
            
            if type(kw['atributos_extra'])==type(u''):
                a=kw['atributos_extra']
                kw['atributos_extra']=[]
                kw['atributos_extra'].append(a)
            for id in kw['atributos_extra']:
                log.debug('id = %s' %str(id))
                aeo          =   DBSession.query(AtributoExtra).filter_by(id=int(id)).first()
                aen          =   AtributoExtra()
                aen.valor    =   kw['atributos_extra_'+str(id)]
                aen.campo_extra_id  =   aeo.campo_extra_id
                DBSession.add(aen)
                item.atributos_extra.append(aen)
                log.debug('ae = %s' %str(aen))
                log.debug('attr extra valor = %s' %str(kw['atributos_extra_'+id]))
                log.debug('attr extra id = %s' %str(id))
        else:
            for ae in i.atributos_extra:
                aen          =   AtributoExtra()
                aen.valor    =   ae.valor
                aen.campo_extra_id  =   ae.campo_extra_id
                DBSession.add(aen)
                item.atributos_extra.append(aen)
           
        if kw.has_key('padres'):
            item.padres=[]             
            for id in kw['padres']:
                p=DBSession.query(Item).filter_by(id=int(id)).first()
                item.padres.append(p)
        else:
            if kw.has_key('name'):
                item.padres=[]
            else:
                item.padres=[]             
                for p in i.padres:
                    item.padres.append(p)                
        
        if kw.has_key('antecesores'):
            item.antecesores=[]             
            for id in kw['antecesores']:
                a=DBSession.query(Item).filter_by(id=int(id)).first()
                item.antecesores.append(a)
        else:
            if kw.has_key('name'):            
                item.antecesores=[]
            else:
                for a in i.antecesores:
                    item.antecesores.append(a)
        
        
        if adjunto_id==None:
            for a in i.adjuntos:
                adjunto=Adjunto()
                adjunto.name    =   a.name
                adjunto.filecontent =   a.filecontent
                adjunto.item    =   item
                DBSession.add(adjunto)
        else:
            for a in i.adjuntos:
                if adjunto_id!=a.id:
                    adjunto=Adjunto()
                    adjunto.name    =   a.name
                    adjunto.filecontent =   a.filecontent
                    adjunto.item    =   item
                    DBSession.add(adjunto)
                                
        return item        
        
    @expose()
    def put(self, *args, **kw):
        """update"""
        log.debug('-------- PUTTING --------')
        log.debug('kw-> kw = %s' %str(kw))
        log.debug('ARGS %s' %str(args))
        
        pks = self.provider.get_primary_fields(self.model)
        log.debug('put -> pks = %s' %str(pks))
        
        for i, pk in enumerate(pks):
            if pk not in kw and i < len(args):
                kw['itemid'] = args[i]          
        log.debug('kw-> kw = %s' %str(kw))
        item=self.nueva_version(kw)
        log.debug('kw-> kw = %s' %str(kw))
                           
        DBSession.flush() 


        redirect('/desarrollar/desarrollo_de_fases/?fid='+str(item.fase_id))
        
       
#-----------------------------------------------------------------#
#-------------------Adjunto Controller----------------------------#
#-----------------------------------------------------------------#
    @expose('testando.templates.desarrollar.items.adjunto.index')
    def index(self, *args, **kw):
        itemid=int(kw['itemid'])
        current_files = DBSession.query(Adjunto).filter_by(item_id=itemid)
        referer='/desarrollar/desarrollo_de_fases/?fid='+str(kw['fid'])
        return dict(current_files=current_files,
                    itemid=itemid,referer=referer,title_nav="Desarrollo de Fase")
        
    @expose()
    def save(self, *args, **kw):
        adjunto=Adjunto()
        adjunto.filecontent=kw['userfile'].value
        adjunto.name=kw['userfile'].filename
        item=self.nueva_version(kw)
        DBSession.add(adjunto)
        
        item.adjuntos.append(adjunto)
        DBSession.flush()
        redirect('/desarrollar/items/index/?itemid='+str(item.id)+'&fid='+str(item.fase_id))
    
    @expose(content_type=CUSTOM_CONTENT_TYPE)
    def view(self, fileid):
        try:
            userfile = DBSession.query(Adjunto).filter_by(id=fileid).one()
            iid= userfile.item_id
        except:
            redirect("/")
        content_types = {
            'display': {'.png': 'image/jpeg', '.jpeg':'image/jpeg', '.jpg':'image/jpeg', '.gif':'image/jpeg', '.txt': 'text/plain'},
            'download': {'.pdf':'application/pdf', '.zip':'application/zip','.rar':'application/x-rar-compressed',
                         '.py':'application/text','.c':'application/text','.java':'application/text'}
        }
        for file_type in content_types['display']:
            if userfile.name.endswith(file_type):
                response.headers["Content-Type"] = content_types['display'][file_type]
        for file_type in content_types['download']:
            if userfile.name.endswith(file_type):
                response.headers["Content-Type"] = content_types['download'][file_type]
                response.headers["Content-Disposition"] = 'attachment; filename="'+userfile.name+'"'
        if userfile.name.find(".") == -1:
            response.headers["Content-Type"] = "text/plain"
        return userfile.filecontent
    
        return redirect('/desarrollar/items/index/?itemid='+str(iid)+'&fid='+str('item.fase_id'))
    
    @expose()
    def delete(self, fileid):
        kw={}
        try:           
            adjunto = DBSession.query(Adjunto).filter_by(id=fileid).one()
            kw['itemid']= adjunto.item_id
            item=self.nueva_version(kw,adjunto.id)
            DBSession.flush()
            
        except:
            return redirect('/desarrollar/items/index')

        DBSession.flush()
        return redirect('/desarrollar/items/index/?itemid='+str(item.id)+'&fid='+str(item.fase_id))        
        
        
        
        
        
        
#--------------------------------------------------------------
#-----------------------------------------------------------------#
#-------------------Calculo de Impacto----------------------------#
#-----------------------------------------------------------------#

    @expose('testando.templates.desarrollar.items.impacto.index') 
    def impacto(self, *args, **kw):
        IdActual=int(kw['itemid'])
        ItemActual = DBSession.query(Item).filter_by(id=IdActual).first()
        inombre= ItemActual.name
        calculados=[]
        
        grafo=pgv.AGraph(rankdir='LR')
        grafo.node_attr['shape']='ellipse'
        grafo.node_attr['color']='black'
        grafo.node_attr['style']='filled'
        grafo.node_attr['fillcolor']='#f0f8ff'
        fase = DBSession.query(Fase).filter_by(id=ItemActual.fase_id).first()
        
        grafo.add_node(ItemActual.codigo+"[F"+str(fase.orden)+"] " 
                       + "[" +str(ItemActual.complejidad)
                       +","+str(ItemActual.id)+"]", 
                       fillcolor= 'red')
        
        calculados.append(ItemActual)
        calcular,calculados, grafo = self.calcular_impacto(IdActual, calculados, 0, grafo)

        grafo.layout('dot') # layout with dot
        dir=config['pylons.paths']['static_files']+'/images/'
        log.debug('dir=  %s' %dir)
        grafo.draw(dir+'impacto.png') # write to file 
        log.debug('calculoImpacto = %s' %str(calcular))
        return dict(calcular=calcular,
                    inombre = inombre)
        
        

    @expose()        
    def calcular_impacto(self, IdActual, calculados, calculo, grafo):
        
        ItemActual = DBSession.query(Item).filter_by(id=IdActual).first()
        fase = DBSession.query(Fase).filter_by(id=ItemActual.fase_id).first()
        if(ItemActual not in calculados):
            grafo.add_node(ItemActual.codigo+"[F"+str(fase.orden)+"] " 
                           + "[" +str(ItemActual.complejidad)
                           +","+str(ItemActual.id)+"]")
            calculados.append(ItemActual)
            
        calculo= calculo + ItemActual.complejidad
        
        padres=ItemActual.padres
        antecesores=ItemActual.antecesores
        hijos=ItemActual.hijos
        sucesores=ItemActual.sucesores
        
        # relacion de padres y antecesores
        if(len(padres)!=0):
            for p in padres:
                f = DBSession.query(Fase).filter_by(id=p.fase_id).first()
                grafo.add_edge(p.codigo+"[F"+str(f.orden)+"] " 
                                  + "[" +str(p.complejidad)
                                  +","+str(p.id)+"]",
                                  ItemActual.codigo+"[F"+str(fase.orden)+"] " 
                                  + "[" +str(ItemActual.complejidad)
                                  +","+str(ItemActual.id)+"]", 
                                  color='blueviolet', label='padre-hijo')
               
                if(p not in calculados):
                    
                    calculo , calculados,grafo = self.calcular_impacto(p.id, calculados, calculo, grafo)
        
        if(len(antecesores)!=0):
            
            for a in antecesores:
                f = DBSession.query(Fase).filter_by(id=a.fase_id).first()
                grafo.add_edge(a.codigo+"[F"+str(f.orden)+"] " 
                                  + "[" +str(a.complejidad)
                                  +","+str(a.id)+"]",
                                  ItemActual.codigo+"[F"+str(fase.orden)+"] " 
                                  + "[" +str(ItemActual.complejidad)
                                  +","+str(ItemActual.id)+"]", 
                                  color='green', label='antecesor-sucesor')
                if(a not in calculados):
                    calculo, calculados, grafo = self.calcular_impacto(a.id, calculados, calculo, grafo)
                   
        #relacion de hijos y sucesores
        if(len(hijos)!=0):
            for h in hijos:
                f = DBSession.query(Fase).filter_by(id=h.fase_id).first()
                grafo.add_edge(ItemActual.codigo+"[F"+str(fase.orden)+"] " 
                                  + "[" +str(ItemActual.complejidad)
                                  +","+str(ItemActual.id)+"]",
                                  h.codigo+"[F"+str(f.orden)+"] " 
                                  + "[" +str(h.complejidad)
                                  +","+str(h.id)+"]", 
                                  color='blueviolet', label='padre-hijo')
                if(h not in calculados):
                    calculo , calculados,grafo = self.calcular_impacto(h.id, calculados, calculo, grafo)
                   
        if(len(sucesores)!=0):
            for s in sucesores:
                f = DBSession.query(Fase).filter_by(id=s.fase_id).first()
                grafo.add_edge(ItemActual.codigo+"[F"+str(fase.orden)+"] " 
                                  + "[" +str(ItemActual.complejidad)
                                  +","+str(ItemActual.id)+"]",
                                  s.codigo+"[F"+str(f.orden)+"] " 
                                  + "[" +str(s.complejidad)
                                  +","+str(s.id)+"]", 
                                  color='green', label='antecesor-sucesor')
                if(s not in calculados):
                    calculo , calculados,grafo = self.calcular_impacto(s.id, calculados, calculo, grafo)
                   
        return(calculo,calculados, grafo)
    