from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller,EditFormFiller
from sprox.formbase import AddRecordForm, EditableForm,DisabledForm
from sprox.dojo.formbase import DojoEditableForm, DojoAddRecordForm
from sprox.dojo.fillerbase import DojoTableFiller 

from testando.model.tipoitem import TipoItem
from testando.model import DeclarativeBase, metadata, DBSession

from tw.forms import TableForm, TextField, TextArea,HiddenField,Button
from tw.core import WidgetsList
from tw.forms.validators import Int, NotEmpty, DateConverter
from tw.forms.fields import TableFieldSet

class TipoItemViewForm(DisabledForm):
    __model__ = TipoItem
    name = TextField
    descripcion = TextArea
    campos_extra=[]
    __field_attrs__ = {'descripcion':{'rows':'2','disabled':'disabled'},'name':{'disabled':'disabled'}}
    
tipoitem_view_form = TipoItemViewForm(DBSession) 

class TipoItemAddForm(AddRecordForm):
    __model__ = TipoItem
    __omit_fields__ = ['fecha_creacion', 'items','campos_extra','importado_id']
    btn = Button("add_more_attr", attrs=dict(onclick="javascript:add_more_atrr();",value='Agregar Atributos extras'))
    name = TextField
    fase = HiddenField('fase_id')
    descripcion = TextArea
tipoitem_add_form = TipoItemAddForm(DBSession)    

class TipoItemEditFiller(EditFormFiller):
    __model__ = TipoItem
tipoitem_edit_filler=TipoItemEditFiller(DBSession)
   
class TipoItemEditForm(DojoEditableForm):
    __model__ = TipoItem
    name = TextField
    __omit_fields__ = ['fecha_creacion', 'items', 'fases','importado_id','fase','campos_extra']
    __field_attrs__ = {'descripcion':{'rows':'2'}}
tipoitem_edit_form=TipoItemEditForm(DBSession)
