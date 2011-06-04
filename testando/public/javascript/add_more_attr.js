function add_more_atrr()
{	var index = $('tr').size()
	var newRow = $('<tr id="new_attr_label.container" class="even" title="">'+
	'<td class="labelcol">'+
	'<label id="new_attr_nombre_label" class="fieldlabel" for="new_attr_nombre">Nombre</label>'+
	'</td>'+
	'<td class="labelcol">'+
	'<label id="new_attr_tipo.label" class="fieldlabel" for="new_attr_tipo">Tipo</label>'+
	'</td>	</tr>'+
	
	'<tr id="new_attr_container" class="odd" title="">'+
	'<td class="fieldcol">'+
	'<input id="new_attr_nombre" class="textfield" type="text" value="" name="nombre['+index+']">'+
	'</td>'+
	'<td class="fieldcol">'+
	'<select name="tipo['+index+']">'+
	'<option>Texto</option>'+
	'<option>Fecha</option>'+
	'<option>Numero</option>'+
	'</select>'+
	'</td> <td>'+
	'<input type="button" onclick="$(this).parent().parent().prev().remove();$(this).parent().parent().remove();" value="quitar" id="remove_this_attr" class="button">'
	+'</td> </tr>');
	
	$(".submitbutton").before(newRow);

}