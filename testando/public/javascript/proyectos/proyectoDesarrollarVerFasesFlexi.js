$(function()
{
	$("#proyectoDesarrollarVerFasesFlexi").flexigrid(
	{
		url: '/desarrollar/fases_asignadas/?pid='+$('input#pid').val(),
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : false, align: 'left'},			
			{display: 'Estado', name : 'estado', width : 150, sortable : true, align: 'left'},
			{display: 'Orden', name : 'orden', width : 150, sortable : true, align: 'left'},
		],
		
		buttons : [
			{separator: true},
			{name: 'Acceder a la Fase', bclass: 'enter', onpress : doCommandFases},
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
		title: "Fases a las que perteneces en el proyecto: "+$('#proyectoNombre').val(),
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
		$('.trSelected', grid).each(function()
		{		
			var id = $(this).attr('id');
			idf = id.substring(id.lastIndexOf('row')+3);
			window.location = "/desarrollar/desarrollo_de_fases/?fid="+idf
		});
		
	}
	else
	{msg_falta_seleccion();}

}
function msg_falta_seleccion(){
	jQuery.noticeAdd({
	              text: "Debe seleccionar una Fase!",
	              stay: false,
	              stayTime: 2500,
	              type: "notice"
	    	  });
}