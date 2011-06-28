$(function()
{
	$("#proyectoVerFasesFlexi").flexigrid(
	{
		url: '/configurar/proyectos/fases_asignadas/?pid='+$('input#pid').val(),
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
			{name: 'Usuarios', bclass: 'users', onpress : doCommandFases},
			{separator: true},	
			{separator: true},
			{separator: true},	
			{name: 'Tipos de Items', bclass: 'itemtypes', onpress : doCommandFases},		
			{separator: true},	
			{separator: true},
			{separator: true},
			{name: 'Items', bclass: 'items', onpress : doCommandFases},
			{separator: true},	
			{separator: true},
			{separator: true},
			{name: 'Lineas Base', bclass: 'baselines', onpress : doCommandFases},
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
		title: "Fases del proyecto: "+$('#proyectoNombre').val() + " (iniciado)",
		useRp: true,
		rp: 5,
		showTableToggleBtn: true,
		showToggleBtn: true,
		height: 'auto',
		singleSelect: true,
	});
});

function doCommandFases(com, grid) {
	if ($('.trSelected', grid).length > 0)
	{
		if (com == 'Usuarios')
		{ver_usuarios(grid);}		
		else if (com == 'Tipos de Items')
		{ver_tipos_de_item(grid);}
		else if (com == 'Items')
		{ver_items(grid);}
		else if (com == 'Lineas Base')
		{ver_lineas_base(grid);}						
	}
	else
	{msg_falta_seleccion();}

}
function ver_usuarios(grid){
	$('.trSelected', grid).each(function()
	{	
		id = get_id(this) 
		window.location = "/configurar/vista_de_usuarios/?fid="+id
	});	
}

function ver_tipos_de_item(grid){
	$('.trSelected', grid).each(function()
	{	
		id = get_id(this) 
		estado=get_estado()
		window.location = "/configurar/vista_de_tiposDeItem/?fid="+id
	});	
}

function ver_items(grid){
	$('.trSelected', grid).each(function()
	{	
		id = get_id(this) 
		estado=get_estado()
		window.location = "/configurar/vista_de_items/?fid="+id
	});	
}
function ver_lineas_base(grid){
	$('.trSelected', grid).each(function()
	{	
		id = get_id(this) 
		window.location = "/configurar/vista_de_lineasbase/?fid="+id
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