$(function()
{
	$("#rolesAdministrarFlexi").flexigrid(
	{
		url: '/administrar/lista_de_roles/',
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Permisos', name : 'permisos', width : 150, sortable : false, align: 'left'}
		],
		
		buttons : [
			{separator: true},
			{name: 'Crear', bclass: 'add', onpress : doCommandRol},
			{separator: true},
			{name: 'Editar', bclass: 'edit', onpress : doCommandRol},
			{separator: true},
			{name: 'Borrar', bclass: 'delete', onpress : doCommandRol},
			{separator: true}
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Lista de Roles",
		useRp: true,
		rp: 10,
		showTableToggleBtn: true,
		resizable: false,
		height: 'auto',
		singleSelect: true
	});
});
function doCommandRol(com, grid)
{
	if (com == 'Crear')
	{window.location = location+"new/";}
	else if ($('.trSelected', grid).length > 0)
	{
		if (com == 'Editar')
		{
			var id = $('.trSelected', grid).attr('id');
			id = id.substring(id.lastIndexOf('row')+3);
			window.location = location+id+"/edit/";	
		}
		else if (com == 'Borrar')
		{
			var nombre = $('.trSelected', grid).find('td[abbr="name"]').children().text()	
			var id = $('.trSelected', grid).attr('id');
			id = id.substring(id.lastIndexOf('row')+3);
			if(confirm('Seguro que desea BORRAR el rol: "' + nombre + '" ?'))
			{
				deleteR(id);
			}			
		}
			
	}	
	else{
		msg_falta_seleccion('un rol')
	}
}
function deleteR(id)
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
    	  $("#rolesAdministrarFlexi").flexReload();
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