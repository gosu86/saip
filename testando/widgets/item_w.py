from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller,EditFormFiller
from sprox.formbase import AddRecordForm, EditableForm
from sprox.dojo.formbase import DojoEditableForm, DojoAddRecordForm
from sprox.dojo.fillerbase import DojoTableFiller

from testando.model.item import Item
from testando.model import DeclarativeBase, metadata, DBSession

from tw.forms import TableForm, TextField, TextArea,HiddenField
from tw.core import WidgetsList
from tw.forms.validators import Int, NotEmpty, DateConverter

class ItemAddForm(DojoAddRecordForm):
    __model__ = Item
    __omit_fields__= ['id', 'fecha_creacion', 'tipo_item', 'linea_base']
    name = TextField
    
    submit_text = 'Guardar'
item_add_form = ItemAddForm(DBSession)    

class ItemEditFiller(EditFormFiller):
    __model__ = Item
item_edit_filler=ItemEditFiller(DBSession)
   
class ItemEditForm(DojoEditableForm):
    __model__ = Item
    name = TextField
    __field_attrs__ = {'descripcion':{'rows':'2'}}
item_edit_form=ItemEditForm(DBSession)
