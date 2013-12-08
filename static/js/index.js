var showLinks = function (data){

    var link_list = $.parseJSON(data);
    var data = ''
    $('#linkList').empty()
        $.each(link_list, function(index, value){
        if(value.length > 50)
            data = value.substr(0, 47) + '...'
        else
            data = value

	    $("#linkList").append("<li class=\"downloadLinks\">" + data + "<button id=\"btn_remove_link\"> </button></li>");
                        
    });




}
var Download = function(){
		var that = this;
		var registerError = function(XMLHttpRequset, textStatus, errorThrown)
		{

		};
		var registerSuccess = function(data, textStatus, XMLHttpRequest)
		{
            showLinks(data);
		    return;
		};
		
		var buttonPress = function()
		{
				var downloadLink = {'link':$("#add_link").val()};
				if(downloadLink.link == ''){
						alert("Empty Link!");
						return;
				}
					
				$("#add_link").val('');
			
				$.ajax({data:downloadLink, dataType:"text", error: registerError, success: registerSuccess, type: "POST", url:"/add_link/"});
		};
		
		return{
			buttonPress : buttonPress
		}
			
	
}();

var RemoveLink = function(){
		var that = this;
		var registerError = function(XMLHttpRequset, textStatus, errorThrown)
		{

		};
		var registerSuccess = function(data, textStatus, XMLHttpRequest)
		{
            showLinks(data);
		    return;
		};
		
		var removeButtonPress = function()
		{
				var downloadLink = {'link':$(this)[0].parentNode.innerText};
				if(downloadLink.link == ''){
						alert("Empty Link!");
						return;
				}
				$("#add_link").val('');
			
				$.ajax({data:downloadLink, dataType:"text", error: registerError, success: registerSuccess, type: "POST", url:"/remove_link/"});
		};
		
		return{
			removeButtonPress : removeButtonPress
		}
			
	
}();


$(document).ready(function() {

	$("#btn_add_link").click(Download.buttonPress);
    $("#btn_remove_link").click(RemoveLink.removeButtonPress);
    $("#add_link").click(function(){
        if ($(this).attr('in') == 'false')
        {    
            $(this).val('');
            $(this).attr('in', 'true');
        }
    });
    
//    $(".downloadLinks").each(function(){
//    		$(this).text(decodeURIComponent($(this).text()));
//        if ($(this).text().length > 50) {
//            $(this).text($(this).text().substr(0, 47));
//            $(this).append('...');
//        }
//    });
//	}

});
