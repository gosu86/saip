$(function()
{
	$("#fasesConfigurarFlexi").flexigrid(
	{
		url: location+'lista_de_fases/',
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Estado', name : 'estado', width : 150, sortable : true, align: 'left'},
			{display: 'Orden', name : 'orden', width : 150, sortable : true, align: 'left'}
		],
		
		buttons : [
			{separator: true},
			{name: 'Asignar Tipos De Item', bclass: 'addRemove', onpress : doCommandFases},
			{separator: true}
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Lista de Fases",
		useRp: true,
		rp: 10,
		showTableToggleBtn: true,
		height: 'auto',
		singleSelect: true
	});
});
function doCommandFases(com, grid)
{
	if (com == 'Asignar Tipos De Item')
	{
		if ($('.trSelected', grid).length > 0)
		{
			/*$(".TablaFases").toggle()*/
			$('.gDiv',grid).toggleClass('hideBody');
			$('.trSelected', grid).each(function()
			{
				var id = $(this).attr('id');
				id = id.substring(id.lastIndexOf('row')+3);
				window.location = location+"seleccionar_tiposDeItem/"+id
			});
		}
		else
		{
	    	  jQuery.noticeAdd(
	    	    	  {
	    	              text: 'Debe Seleccionar una fase!.',
	    	              stay: false,
	    	              stayTime: 5000,
	    	              type: 'notice'
	    	    	  });
		}		
		
	}
}