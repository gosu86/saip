$(function()
{
	$("#fasesAsignadasFlexi").flexigrid(
	{
		url: '/configurar/fases_asignadas',
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
			{name: 'Quitar', bclass: 'delete', onpress : doCommandAsignadas},
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
		title: "Fases Asignadas",
		useRp: true,
		rp: 5,
		showTableToggleBtn: true,
		height: 'auto',
		singleSelect: false,
		query: $('input[type="hidden"]').val(),
		qtype: 'proyecto_id',
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
    	  
    	  $("#fasesAsignadasFlexi").flexReload();
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
    	  $("#fasesAsignadasFlexi").flexReload();
    	  jQuery.noticeAdd(
    	    	  {
    	              text: data.msg,
    	              stay: false,
    	              stayTime: 5000,
    	              type: data.type
    	    	  });
    	  
    	  $("#fasesDisponiblesFlexi").flexReload();
    	 
      },
    });
}


function doCommandAsignadas(com, grid) {
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