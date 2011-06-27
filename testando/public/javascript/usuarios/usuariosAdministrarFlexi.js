$(function()
{
	$("#usuariosAdministrarFlexi").flexigrid(
	{
		url: '/administrar/lista_de_usuarios/',
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Apellido', name : 'apellido', width : 150, sortable : true, align: 'left'},
			{display: 'Email', name : 'email', width : 150, sortable : true, align: 'left'},
			{display: 'Estado', name : 'estado', width : 150, sortable : true, align: 'left'}
		],
		
		buttons : [
			{separator: true},
			{name: 'Crear', bclass: 'add', onpress : doCommandUsuario},
			{separator: true},
			{name: 'Editar', bclass: 'edit', onpress : doCommandUsuario},
			{separator: true},
			{name: 'Borrar', bclass: 'delete', onpress : doCommandUsuario},
			{separator: true},
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true},
			{display: 'Apellido', name : 'apellido', isdefault: true},
			{display: 'Email', name : 'email', isdefault: true},
			{display: 'Estado', name : 'estado', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Lista de Usuarios",
		useRp: true,
		rp: 10,
		nowrap: false,
		showTableToggleBtn: true,
		resizable: true,
		height: 'auto',
		singleSelect: true
	});
});
function doCommandUsuario(com, grid)
{
	if (com == 'Crear')
	{window.location = location+"new/";}
	else if ($('.trSelected', grid).length > 0)
	{	
		if (com == 'Editar')
		{
			var id = $('.trSelected', grid).attr('id');
			id = id.substring(id.lastIndexOf('row')+3);
			window.location = location+id+"/edit/"
		}
		else if (com == 'Borrar') 
		{
			var nombre = $('.trSelected', grid).find('td[abbr="name"]').children().text()	
			var id = $('.trSelected', grid).attr('id');
			id = id.substring(id.lastIndexOf('row')+3);
			if(confirm('Seguro que desea BORRAR el usuario: "' + nombre + '" ?'))					
			{
				deleteU(id)
			}
		}
	}
	else
	{msg_falta_seleccion('un usuario')}
	
}
function deleteU(id)
{
    $.ajax(
    {
      type: 'POST',
      dataType: "json",
      url: location+"/post_delete",
      data: {id:id},
      success: function(data)
      {
    	  jQuery.noticeAdd(
    	    	  {
    	              text: data.msg,
    	              stay: false,
    	              stayTime: 5000,
    	              type: data.type
    	    	  });
    	  
    	  $("#usuariosAdministrarFlexi").flexReload();
      },
    });
}
function msg_falta_seleccion(an_element){
	jQuery.noticeAdd({
	              text: "Debe seleccionar al menos "+an_element+"!",
	              stay: false,
	              stayTime: 2500,
	              type: "notice"
	    	  });
}