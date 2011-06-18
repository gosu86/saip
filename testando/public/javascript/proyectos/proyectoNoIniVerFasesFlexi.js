$(function()
{
	$("#proyectoVerFasesFlexi").flexigrid(
	{
		url: '/configurar/fases_asignadas/?pid='+$('input#pid').val(),
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : false, align: 'left'},			
			{display: 'Estado', name : 'estado', width : 150, sortable : true, align: 'left'},
			{display: 'Orden', name : 'orden', width : 50, sortable : true, align: 'left'},
			{display: 'Usuarios', name : 'usuarios', width : 50, sortable : true, align: 'left'},
			{display: 'Tipos de Items', name : 'tiposdeitem', width : 80, sortable : true, align: 'left'},
			{display: 'Items', name : 'items', width : 50, sortable : true, align: 'left'},
		],
		
		buttons : [
			{separator: true},
			{name: 'Crear', bclass: 'add', onpress : doCommandFases},
			{separator: true},
			{name: 'Editar', bclass: 'edit', onpress : doCommandFases},
			{separator: true},
			{name: 'Borrar', bclass: 'delete', onpress : doCommandFases},
			{separator: true},
			{separator: true},		           
			{separator: true},			
			{separator: true},
			{separator: true},		           
			{separator: true},
			{name: 'Usuarios', bclass: 'users', onpress : doCommandFases},
			{separator: true},
			{name: 'Tipos de Items', bclass: 'itemtypes', onpress : doCommandFases},	
			{separator: true},
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true},
			{display: 'Estado', name : 'estado', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		nowrap: false,
		title: "Fases del proyecto: "+$('#proyectoNombre').val() + " (No iniciado)",
		useRp: true,
		rp: 5,
		showTableToggleBtn: true,
		showToggleBtn: true,
		height: 'auto',
		singleSelect: true,
	});
});

function doCommandFases(com, grid) {
	if (com == 'Crear')
	{window.location = "/configurar/fases/new/?proyecto_id="+$('input#pid').val();}
	else if ($('.trSelected', grid).length > 0)
	{
		if (com == 'Editar')
		{
			$('.trSelected', grid).each(function()
			{
				id = get_id(this);
				window.location = '/configurar/fases/'+id+"/edit/";
			});
		}
		else if (com == 'Borrar') 
		{
			$('.trSelected', grid).each(function() {
				nombre = get_nombre();
				id = get_id(this);
				if(confirm('Seguro que desea BORRAR la fase: "' + nombre + '" ?'))
				{deleteF(id);}
			});
		}
		else if (com == 'Usuarios')
		{ver_usuarios(grid);}		
		else if (com == 'Tipos de Items')
		{ver_tipos_de_item(grid);}
		
	}
	else
	{msg_falta_seleccion();}
	


} 

function deleteF(id) {
    $.ajax(
    {
      type: 'POST',
      dataType: "json",
      url: "/configurar/fases/post_delete",
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
    	  
    	  $("#proyectoVerFasesFlexi").flexReload();
      },
    });
}

function ver_usuarios(grid){
	$('.trSelected', grid).each(function()
	{	
		id = get_id(this) 
		nombre=get_nombre()
		window.location = "/configurar/vista_de_usuarios/?fid="+id
	});	
}

function ver_tipos_de_item(grid){
	$('.trSelected', grid).each(function()
	{	
		id = get_id(this) 
		nombre=get_nombre()
		estado=get_estado()
		window.location = "/configurar/vista_de_tiposDeItem/?fid="+id
	});	
}

function get_id(tr){
	var id = $(tr).attr('id');
	id = id.substring(id.lastIndexOf('row')+3);
	return id;
}
 
function get_nombre(){
	nombre=$('.trSelected').find('td[abbr="name"]').text();
	return nombre
}
function get_estado(grid){
	estado=$('.trSelected').find('td[abbr="estado"]').text();
	return estado
} 
function msg_falta_seleccion(){
	jQuery.noticeAdd({
	              text: "Debe seleccionar una Fase!",
	              stay: false,
	              stayTime: 2500,
	              type: "notice"
	    	  });
}