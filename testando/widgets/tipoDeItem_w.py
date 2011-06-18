from sprox.fillerbase import EditFormFiller
from sprox.formbase import EditableForm,AddRecordForm

from testando.model.tipoitem import TipoItem
from testando.model import DBSession

from tw.forms import TextField,TextArea,Button,HiddenField

class TipoItemAddForm(AddRecordForm):
    __model__ = TipoItem
    __omit_fields__ = ['fecha_creacion', 'items', 'fases','campos_extra']
    __field_attrs__ = {'descripcion':{'rows':'2'},'name':{'label':'Nombre: '}}
    btn = Button("add_more_attr", attrs=dict(onclick="javascript:add_more_atrr();",value='Agregar Atributos extras'))
    name = TextField
    descripcion = TextArea
    fase = HiddenField('fase_id')
tipoitem_add_form = TipoItemAddForm(DBSession) 

class TipoItemEditFiller(EditFormFiller):
    __model__ = TipoItem
   
class TipoItemEditForm(EditableForm):
    __model__ = TipoItem
    __omit_fields__ = ['fecha_creacion', 'items', 'fases','importado_id','fase','campos_extra']
    __field_attrs__ = {'descripcion':{'rows':'2'},'name':{'label':'Nombre: '}}
        
    name = TextField

tipoitem_edit_filler    =   TipoItemEditFiller(DBSession)
tipoitem_edit_form      =   TipoItemEditForm(DBSession)
