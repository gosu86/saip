from sprox.dojo.formbase    import DojoEditableForm,DojoAddRecordForm
from sprox.fillerbase       import EditFormFiller

from testando.model         import DBSession
from testando.model.fase    import Fase

from tw.forms import TextField,TextArea
from tw.forms.validators import Int, NotEmpty, DateConverter

from myWidgets import SingleSelectEstadosFases

class FaseNewForm(DojoAddRecordForm):
    __model__       = Fase
    __omit_fields__ = ['estado','fecha_creacion','proyecto', 'tipos_items']
    __field_attrs__ = {'descripcion':{'rows':'2','cols':'30'}}
    orden   =   TextField('orden',validator=Int)
    name    =   TextField('name',label_text='Nombre')
    descripcion = TextArea

class FaseEditFiller(EditFormFiller):
    __model__ = Fase
   
class FaseEditForm(DojoEditableForm):
    __model__       = Fase
    __omit_fields__ = ['fecha_creacion']
    __field_attrs__ = {'descripcion':{'rows':'2','cols':'30'}}
    
    name = TextField
    estado = SingleSelectEstadosFases
    
fase_new_form = FaseNewForm(DBSession)
fase_edit_filler=FaseEditFiller(DBSession)    
fase_edit_form=FaseEditForm(DBSession)