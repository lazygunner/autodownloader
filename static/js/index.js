
var Download = function(){
		var that = this;
		var registerError = function(XMLHttpRequset, textStatus, errorThrown)
		{

		};
		var registerSuccess = function(data, textStatus, XMLHttpRequest)
		{
				var link_list = $.parseJSON(data);
                var data = ''
                $.each(link_list, function(index, value){
                    if(value.length > 50)
                        data = value.substr(0, 47) + '...'
                    else
                        data = value

				    $("#linkList").append("<li class=\"downloadLinks\">" + data + "</li>");
                        
                });

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


$(document).ready(function() {

	$("#btn_add_link").click(Download.buttonPress);
    
//    $(".downloadLinks").each(function(){
//    		$(this).text(decodeURIComponent($(this).text()));
//        if ($(this).text().length > 50) {
//            $(this).text($(this).text().substr(0, 47));
//            $(this).append('...');
//        }
//    });
//	}

});
