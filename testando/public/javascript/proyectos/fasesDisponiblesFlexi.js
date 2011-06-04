$(function()
{
	$("#fasesDisponiblesFlexi").flexigrid(
	{
		url: '/configurar/fases_disponibles',
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
			{name: 'Asignar', bclass: 'add', onpress : doCommandDisponibles},
			{separator: true},
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true},
			{display: 'Estado', name : 'estado', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Fases Disponibles",
		useRp: true,
		rp: 5,
		showTableToggleBtn: true,
		height: 'auto',
		singleSelect: false,
	});
});
function asignar_fases(id) {
    $.ajax(
    {
      type: 'POST',
      dataType: "json",
      url: '/configurar/asignar_fases',
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


function doCommandDisponibles(com, grid) {
	if (com == 'Asignar')
	{
		if ($('.trSelected', grid).length > 0)
		{	
			var proyectoID=''
				
			proyectoID=String(location);
			proyectoID=proyectoID.substr(proyectoID.lastIndexOf('/')+1,4);
			var ids=''
			ids=proyectoID+','
			$('.trSelected', grid).each(function()
			{	
				var id = $(this).attr('id');
				id = id.substring(id.lastIndexOf('row')+3);
				ids=ids+(id+',')
			});
			/*{alert("Ids: "+ids);}*/
			asignar_fases(ids)			
		}
		else
		{
	    	  jQuery.noticeAdd(
	    	    	  {
	    	              text: "Seleccione almenos una fase para asignar!.",
	    	              stay: false,
	    	              stayTime: 3000,
	    	              type: 'notice'
	    	    	  });	
		}
	}

}