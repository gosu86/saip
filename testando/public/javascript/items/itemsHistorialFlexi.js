$(function(){
	$("#itemsHistorialFlexi").flexigrid(
	{	
		url: '/configurar/items_historial/?iid='+$('input#iid').val(),
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
			{name: 'Revertir', bclass: 'goback', onpress : doCommandItem},
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
		
		sortname: "version",
		sortorder: "desc",
		usepager: true,
		title: "Historial del Item: <span class=flexiNameTitle>"+$('#INombre').val()+ '  </span><span class=flexiVersionTitle>Version Actual: '+$('#IVersion').val()+"</span>",
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
			id=get_id($('.trSelected', grid).first())
			if (com == 'Revertir')
			{
				alert('revertir: '+id)
				//revertir(id)
			}
			else if (com == 'Revivir')
			{
				alert('ReVIVIR: '+id)
				//revivir(id)
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

function msg_falta_seleccion(){
	jQuery.noticeAdd({
	              text: "Debe seleccionar al menos un item!",
	              stay: false,
	              stayTime: 2500,
	              type: "notice"
	    	  });
}

function revivir(id){
    $.ajax(
    	    {
    	      type: 'POST',
    	      dataType: "json",
    	      url: '/configurar/aplicar_linea_base',
    	      data: {ids:ids},
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
function revertir(id){
    $.ajax(
    	    {
    	      type: 'POST',
    	      dataType: "json",
    	      url: '/configurar/aplicar_linea_base',
    	      data: {ids:ids},
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