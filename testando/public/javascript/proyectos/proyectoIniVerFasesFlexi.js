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
			{display: 'Orden', name : 'orden', width : 150, sortable : true, align: 'left'}
		],
		
		buttons : [
			{separator: true},
			{name: 'Usuarios', bclass: 'addUsers', onpress : doCommandFases},
			{separator: true},			
			{name: 'Tipos de Items', bclass: 'addItemsType', onpress : doCommandFases},		
			{separator: true},
			{name: 'Items', bclass: 'addItemsType', onpress : doCommandFases},
			{separator: true},
			{name: 'Lineas Base', bclass: 'addItemsType', onpress : doCommandFases},
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
function deleteF(id) {
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
    	  
    	  $("#proyectoVerFasesFlexi").flexReload();
      },
    });
}


function liberar_fases(id) {
    $.ajax(
    {
      type: 'POST',
      dataType: "json",
      url: '/configurar/quitar_fases',
      data: {ids:id},
      success: function(data)
      { 
    	  $("#proyectoVerFasesFlexi").flexReload();
    	  jQuery.noticeAdd(
    	    	  {
    	              text: data.msg,
    	              stay: false,
    	              stayTime: 5000,
    	              type: data.type
    	    	  });
   	 
      },
    });
}


function doCommandFases(com, grid) {
	if (com == 'Quitar')
	{
		if ($('.trSelected', grid).length > 0)
		{	
			var ids=''
			$('.trSelected', grid).each(function()
			{	
				var id = $(this).attr('id');
				id = id.substring(id.lastIndexOf('row')+3);
				ids=ids+(id+',')
			});
			liberar_fases(ids)			
		}
		else
		{
	    	  jQuery.noticeAdd(
	    	    	  {
	    	              text: "Seleccione almenos una fase para liberar!.",
	    	              stay: false,
	    	              stayTime: 3000,
	    	              type: 'notice'
	    	    	  });
		}
	}

}