$(function()
{
	$("#proyectoVerFasesFlexi").flexigrid(
	{
		url: '/configurar/proyectos/fases_asignadas/?pid='+$('input#pid').val(),
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : true, align: 'left'},			
			{display: 'Estado', name : 'estado', width : 150, sortable : true, align: 'left'},
			{display: 'Orden', name : 'orden', width : 50, sortable : true, align: 'left'},
			{display: 'Usuarios', name : 'usuarios', width : 50, sortable : false, align: 'left'},
			{display: 'Tipos de Items', name : 'tiposdeitem', width : 80, sortable : false, align: 'left'},
			{display: 'Items', name : 'items', width : 50, sortable : false, align: 'left'},
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
		id=get_ids(grid)[0]
		if (com == 'Usuarios')
		{window.location = "/configurar/vista_de_usuarios/?fid="+id}		
		else if (com == 'Tipos de Items')
		{window.location = "/configurar/vista_de_tiposDeItem/?fid="+id}
		else if (com == 'Items')
		{window.location = "/configurar/vista_de_items/?fid="+id}
		else if (com == 'Lineas Base')
		{window.location = "/configurar/vista_de_lineasbase/?fid="+id}						
	}
	else
	{notify("Debe seleccionar una fase!",null,timeL)}
}