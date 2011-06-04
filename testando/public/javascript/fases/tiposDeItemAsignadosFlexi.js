$(function()
{
	$("#tiposDeItemAsignadosFlexi").flexigrid(
	{
		url: '/configurar/fases/tiposDeItem_asignados',
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
		],
		
		buttons : [
			{separator: true},
			{name: 'Liberar', bclass: 'delete', onpress : doCommandAsignados},
			{separator: true},
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true},
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		nowrap: false,
		title: "Tipos de Item Asignados",
		useRp: true,
		rp: 5,
		showTableToggleBtn: true,
		height: 'auto',
		singleSelect: false,
		query: $('input[type="hidden"]').val(),
		qtype: 'fase_id',
	});
});
function liberar_tiposDeItem(id) {
    $.ajax(
    {
      type: 'POST',
      dataType: "json",
      url: "/configurar/fases/liberar_tiposDeItem",
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
    	  
    	  $("#tiposDeItemAsignadosFlexi").flexReload();
    	 
      },
    });
}


function doCommandAsignados(com, grid) {
	if (com == 'Liberar')
	{
		if ($('.trSelected', grid).length > 0)
		{	
			var fID=''
				
				fID=String(location);
				fID=fID.substr(fID.lastIndexOf('/')+1,4);
				var ids=''
				ids=fID+','			
			$('.trSelected', grid).each(function()
			{	
				var id = $(this).attr('id');
				id = id.substring(id.lastIndexOf('row')+3);
				ids=ids+(id+',')
			});
			liberar_tiposDeItem(ids)			
		}
		else
		{
	    	  jQuery.noticeAdd(
	    	    	  {
	    	              text: "Seleccione almenos un tipo de item para liberar!.",
	    	              stay: false,
	    	              stayTime: 3000,
	    	              type: 'notice'
	    	    	  });
		}
	}

}