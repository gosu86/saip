$(function()
{
	$("#tiposDeItemDisponiblesFlexi").flexigrid(
	{
		url: '/configurar/fases/tiposDeItem_disponibles',
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'}
		],
		
		buttons : [
			{separator: true},
			{name: 'Asignar', bclass: 'add', onpress : doCommandDisponibles},
			{separator: true},
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Tipos de Item Disponibles",
		useRp: true,
		rp: 5,
		showTableToggleBtn: true,
		height: 'auto',
		singleSelect: false,
	});
});
function asignar_tiposDeItem(id) {
    $.ajax(
    {
      type: 'POST',
      dataType: "json",
      url: "/configurar/fases/asignar_tiposDeItem",
      data: {ids:id},
      success: function(data)
      { 
    	  $("#tiposDeItemAsignadosFlexi").flexReload();
    	  jQuery.noticeAdd(
    	    	  {
    	              text: data.msg,
    	              stay: false,
    	              stayTime: 5000,
    	              type: data.type
    	    	  });
    	  
    	  $("#tiposDeItemDisponiblesFlexi").flexReload();
    	 
      },
    });
}


function doCommandDisponibles(com, grid) {
	if (com == 'Asignar')
	{
		if ($('.trSelected', grid).length > 0)
		{	
			var faseID=''
				
			faseID=String(location);
			faseID=faseID.substr(faseID.lastIndexOf('/')+1,4);
			var ids=''
			ids=faseID+','
			$('.trSelected', grid).each(function()
			{	
				var id = $(this).attr('id');
				id = id.substring(id.lastIndexOf('row')+3);
				ids=ids+(id+',')
			});
			{alert("Ids: "+ids);}
			asignar_tiposDeItem(ids)			
		}
		else
		{
	    	  jQuery.noticeAdd(
	    	    	  {
	    	              text: "Seleccione almenos un tipo de item para asignar!.",
	    	              stay: false,
	    	              stayTime: 3000,
	    	              type: 'notice'
	    	    	  });	
		}
	}

}