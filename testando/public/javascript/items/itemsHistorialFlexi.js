$(function(){
	$("#itemsHistorialFlexi").flexigrid(
	{	
		url: '/desarrollar/items/historial/?iid='+$('input#iid').val(),
		dataType: 'json',
		
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Codigo', name : 'codigo', width : 50, sortable : true, align: 'left'},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Version', name : 'version', width : 60, sortable : true, align: 'left'},			
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : true, align: 'left'},
			{display: 'Complejidad', name : 'complejidad', width : 100, sortable : true, align: 'left'},
			{display: 'Estado', name : 'estado', width : 100, sortable : true, align: 'left'},
			{display: 'Tipo De Item', name : 'tipoDeItem', width : 150, sortable : true, align: 'left'},
			{display: 'Padres', name : 'padres', width : 100, sortable : true, align: 'left'},
			{display: 'Hijos', name : 'hijos', width : 100, sortable : true, align: 'left'},
			{display: 'Antecesores', name : 'antecesores', width : 100, sortable : true, align: 'left'},
			{display: 'Sucesores', name : 'sucesores', width : 100, sortable : true, align: 'left'},
		],
		
		buttons : [	           
			{separator: true},
			{name: 'Revertir', bclass: 'goback', onpress : doCommandItem},
			{separator: true},

			
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name'},
			{display: 'Estado', name : 'estado'},
			{display: 'Version', name : 'version'},
			{display: 'Codigo', name : 'codigo', isdefault: true}
		],
		
		sortname: "version",
		sortorder: "desc",
		usepager: true,
		title: "Historial del Item: <span class=flexiNameTitle>"+$('#INombre').val()+ '  </span>'+
		'<span class=flexiVersionTitle>Version Actual: '+$('#IVersion').val()+"</span>"+
		'<span class="flexiEstadoTitle '+$('#IEstado').val()+'"> Estado: '+$('#IEstado').val()+"</span>",
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
		if ($('input#IEstado').val()=='Eliminado'){
			msg_eliminado()	
		}
		else{
			id=$('input#iid').val()+','
			id=id+get_id($('.trSelected', grid).first())
			if (com == 'Revertir')
			{
				revertir(id)
			}	
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


function revertir(id){
    $.ajax(
    	    {
    	      type: 'POST',
    	      dataType: "json",
    	      url: '/desarrollar/items/revertir',
    	      data: {id:id},
    	      success: function(data)
    	      {

    	        	  jQuery.noticeAdd(
    	        	    	  {
    	        	              text: data.msg,
    	        	              stay: false,
    	        	              stayTime: 5500,
    	        	              type: data.type
    	        	    	  });
    	        	 
    	        if (data.reload)
    	        { 
    	        	window.location='/'+$('a.active').text().toLowerCase()+'/items/vista_de_historial/?iid='+data.id.toString()
    	        }
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

function msg_eliminado(){
	jQuery.noticeAdd({
	              text: "La version actual del item tiene estado eliminado.",
	              stay: false,
	              stayTime: 3000,
	              type: "notice"
	    	  });
	jQuery.noticeAdd({
	              text: "No se pueden revertir items eliminados.",
	              stay: false,
	              stayTime: 2500,
	              type: "error"
	    	  });	    	  
}