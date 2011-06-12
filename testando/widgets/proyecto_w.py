from sprox.dojo.formbase    import DojoEditableForm,DojoAddRecordForm
from sprox.fillerbase       import EditFormFiller

from testando.model             import DBSession
from testando.model.proyecto    import Proyecto

from tw.forms import TextField, InputField,SingleSelectField
from tw.forms.validators import Int, NotEmpty, DateConverter

from myWidgets import SingleSelectEstadosProyectos

   
class ProyectoNewForm(DojoAddRecordForm):
    __model__           =   Proyecto
    __field_attrs__     =   {'descripcion':{'rows':'2'},'lider_id':{'label':'Lider'}}
    __omit_fields__     =   ['fecha_creacion','fases','usuarios','estado']
    __require_fields__  =   ['lider']
    
    #lider_id = TextField('lider_id',label_text="Lider")
    name = TextField('name', label_text='Nombre: ')
    empresa = TextField
    
class ProyectoEditFiller(EditFormFiller):
    __model__ = Proyecto
    __omit_fields__     =   ['fecha_creacion','usuarios']
    
class ProyectoEditForm(DojoEditableForm):
    __model__           = Proyecto
    __field_attrs__     = {'descripcion':{'rows':'2'},'fases':{'display':'none'}}
    __omit_fields__     = ['fecha_creacion','fases','usuarios']
    __require_fields__  =   ['lider','lider_id']
    
    #lider_id = TextField('lider_id',label_text="Lider")
    name = TextField('name', label_text='Nombre: ')
    empresa = TextField
    estado = SingleSelectEstadosProyectos
    
proyecto_new_form = ProyectoNewForm(DBSession)    
proyecto_edit_filler=ProyectoEditFiller(DBSession)
proyecto_edit_form=ProyectoEditForm(DBSession)