$(function()
{
	$("#menuMisProyectosFlexi").flexigrid(
	{
		url: '/mis_proyectos/',
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : false, align: 'left'},
			{display: 'Estado', name : 'estado', width : 150, sortable : true, align: 'left'},
			{display: 'Fases', name : 'fases', width : 150, sortable : false, align: 'left'}
		],
		
		buttons : [
			{separator: true},         
			{name: 'Acceder', bclass: 'add', onpress : doCommandProyecto},
			{separator: true},
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true},
			{display: 'Estado', name : 'estado', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Mis Proyectos",
		useRp: true,
		rp: 10,
		showTableToggleBtn: true,
		height: 'auto',
		singleSelect: true
	});
});

function doCommandProyecto(com, grid)
{
	if (com == 'Acceder') {window.location = location+"new/";}
}