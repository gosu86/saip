$(function(){
	$("#faseVerItemsFlexi").flexigrid(
	{	
		url: '/configurar/items_creados/?fid='+$('input#fid').val(),
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Version', name : 'version', width : 60, sortable : true, align: 'left'},			
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : true, align: 'left'},
			{display: 'Complejidad', name : 'complejidad', width : 100, sortable : true, align: 'left'},
			{display: 'Estado', name : 'estado', width : 100, sortable : true, align: 'left'},
			{display: 'Tipo De Item', name : 'tipoDeItem', width : 150, sortable : true, align: 'left'},			
		],
		
		buttons : [	           
			{separator: true},
			{name: 'Ver Historial', bclass: 'history', onpress : doCommandItem},
			{separator: true},
			{separator: true},
			{separator: true},
			{name: 'Revivir', bclass: 'reborn', onpress : doCommandItem},
			{separator: true},			
			
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true},
			{display: 'Estado', name : 'estado', isdefault: true},
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		title: "Items de la fase: "+$('#fNombre').val(),
		useRp: true,
		rp: 5,
		showTableToggleBtn: true,
		height: 'auto',
		singleSelect: true
	});	
});


function doCommandItem(com, grid)
{
	if ($('.trSelected', grid).length > 0)
	{	
			id = get_id($('.trSelected', grid))
			if (com == 'Ver Historial')
			{
					window.location = '/configurar/historial/?iid='+id;
			}
			else if (com == 'Revivir')
			{
				revivir(id)
			}			
	}
	else
	{msg_falta_seleccion()}

}

function get_id(tr){
	var id = $(tr).attr('id');
	id = id.substring(id.lastIndexOf('row')+3);
	return id;
}

function revivir(id){
    $.ajax(
    	    {
    	      type: 'POST',
    	      dataType: "json",
    	      url: '/configurar/revivir',
    	      data: {id:id},
    	      success: function(data)
    	      { 
    	        	  jQuery.noticeAdd(
    	        	    	  {
    	        	              text: data.msg,
    	        	              stay: false,
    	        	              stayTime: 2500,
    	        	              type: data.type
    	        	    	  });    	        		  
    	        	  $("#faseVerItemsFlexi").flexReload();
    	      }
    	    	 
    	    });	
}



function msg_falta_seleccion(){
	jQuery.noticeAdd({
	              text: "Debe seleccionar al menos un item!",
	              stay: false,
	              stayTime: 2500,
	              type: "notice"
	    	  });
}