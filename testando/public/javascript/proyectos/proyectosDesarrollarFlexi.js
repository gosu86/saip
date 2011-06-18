$(function()
{
	function checkProyectos(data) {
		if (data.total == 0)
		{
			jQuery.noticeAdd(
			    	  {
			              text: "Ud. no posee proyectos iniciados...",
			              stay: false,
			              stayTime: 5000,
			              type: "notice"
			    	  });		
		}
		return data
	}	
	
	$("#proyectosDesarrollarFlexi").flexigrid(
	{
		url: '/desarrollar/lista_de_proyectos/',
		dataType: 'json',
		colModel : [
			{display: 'ID', name : 'id', width : 40, sortable : true, align: 'left', hide : true},
			{display: 'Nombre', name : 'name', width : 150, sortable : true, align: 'left'},
			{display: 'Lider', name : 'lider', width : 150, sortable : false, align: 'left'},
			{display: 'Descripcion', name : 'descripcion', width : 150, sortable : false, align: 'left'},
			{display: 'Empresa', name : 'empresa', width : 150, sortable : false, align: 'left'},
		],

		buttons : [
			{separator: true},         
			{name: 'Acceder al Proyecto', bclass: 'enter',width : 150, onpress : doCommandFases},
		],
		
		searchitems : [
			{display: 'Nombre', name : 'name', isdefault: true},
			{display: 'Estado', name : 'estado', isdefault: true}
		],
		
		sortname: "id",
		sortorder: "asc",
		usepager: true,
		nowrap: false,
		title: "Proyectos a los que perteneces",
		useRp: true,
		rp: 10,
		showTableToggleBtn: true,
		height: 'auto',
		singleSelect: true,
		preProcess: checkProyectos,
	});
});

function doCommandFases(com, grid)
{
	if (com == 'Acceder al Proyecto')
	{
		if ($('.trSelected', grid).length > 0)
		{
			$('.trSelected', grid).each(function()
			{
				var id = $(this).attr('id');
				id = id.substring(id.lastIndexOf('row')+3);
				window.location = "/desarrollar/vista_de_fases/?pid="+id
			});
		}
		else
		{
	    	  jQuery.noticeAdd(
	    	    	  {
	    	              text: 'Debe Seleccionar un proyecto!.',
	    	              stay: false,
	    	              stayTime: 3000,
	    	              type: 'notice'
	    	    	  });
		}		
		
	}
	else if (com == 'Iniciar')
	{
		if ($('.trSelected', grid).length > 0)
		{	var nombre = $('.trSelected',"#proyectosDesarrollarFlexi").find('td[abbr="name"]').children().text()	
			$('.trSelected', grid).each(function()
			{
				var id = $(this).attr('id');
				id = id.substring(id.lastIndexOf('row')+3);
				fases=$('div','.trSelected',grid).last().text()
				if (fases.length >1)
				{
					iniciarP(id)
				}
				else
				{
					jQuery.noticeAdd(
					    	  {
					              text: "El proyecto seleccionado no posee fases. No se puede iniciar.",
					              stay: false,
					              stayTime: 3000,
					              type: "error"
					    	  });					
				}
			});
		}
		else{
			jQuery.noticeAdd(
			    	  {
			              text: "Debe seleccionar una fila para iniciar!",
			              stay: false,
			              stayTime: 5000,
			              type: "notice"
			    	  });			
		}		
	}
}
function iniciarP(id) {
    $.ajax(
    {
      type: 'POST',
      dataType: "json",
      url: location+"/iniciar_proyecto",
      data: {id:id},
      success: function(data)
      {
    	  jQuery.noticeAdd(
    	  {
              text: data.msg,
              stay: false,
              stayTime: 2000,
              type: data.type
    	  });
    	  
    	  $("#proyectosDesarrollarFlexi").flexReload();
    	  
      },
    });
}