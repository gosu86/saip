$(function(){
	$("#fasesVerItemsEliminadosFlexi").flexigrid(
	{	
		url: '/desarrollar/fases/items_creados/?fid='+$('input#fid').val()+'&solo_e=true',
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Codigo', name : 'codigo', width : 50, sortable : true, align: 'left'},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Version', name : 'version', width : 50, sortable : true, align: 'left'},			
			{display: 'Estado', name : 'estado', width : 100, sortable : true, align: 'left'},			
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : true, align: 'left'},
			{display: 'Complejidad', name : 'complejidad', width : 80, sortable : true, align: 'left'},
			{display: 'Tipo De Item', name : 'tipoDeItem', width : 150, sortable : true, align: 'left'},
			{display: 'Linea Base', name : 'lineabase', width : 150, sortable : true, align: 'left'},
		],
		
		buttons : [	           
			{separator: true},
			{name: 'Revivir', bclass: 'reborn', onpress : doCommandItemEliminado},
			{separator: true},			
			
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name'},
			{display: 'Version', name : 'version'},
			{display: 'Codigo', name : 'codigo', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Items Eliminados",
		useRp: true,
		rp: 5,
		showTableToggleBtn: true,
		height: 'auto',
		singleSelect: true
	});	
	
	$('div.TablaItemsEliminados .flexigrid').addClass('hideBody');
});


function doCommandItemEliminado(com, grid)
{
	if ($('.trSelected', grid).length > 0)
	{	
			id = get_id($('.trSelected', grid))

			if (com == 'Revivir')
			{
				revivir(id)
			}			
	}
	else
	{msg_falta_seleccion()}

}
function revivir(id)
{
		window.location = '/desarrollar/items/'+id+'/edit/'
}
