$(function()
{
	$("#permisosAdministrarFlexi").flexigrid(
	{
		url: '/administrar/lista_de_permisos/',
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'permiso_name', width : 150, sortable : true, align: 'left'},
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : false, align: 'left'},
			{display: 'Roles al que pertenece', name : 'roles', width : 150, sortable : false, align: 'left'}
		],

		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true},
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Lista de Permisos",
		useRp: true,
		rp: 10,
		showTableToggleBtn: true,
		resizable: false,
		height: 'auto',
		singleSelect: true
	});
});
function doCommandPermiso(com, grid)
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
			var nombre = $('.trSelected', grid).find('td[abbr="permiso_name"]').children().text()	
			var id = $('.trSelected', grid).attr('id');
			id = id.substring(id.lastIndexOf('row')+3);
			if(confirm('Seguro que desea BORRAR el permiso: "' + nombre + '" ?'))
			{
				deletePER(id)
			}
		}
	}
	else
	{
		msg_falta_seleccion('un permiso')
	}
	
}
function deletePER(id) {
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
    	              stayTime: 3000,
    	              type: data.type
    	    	  });    	  
    	  $("#permisosAdministrarFlexi").flexReload();
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