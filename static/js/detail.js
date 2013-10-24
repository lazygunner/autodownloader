
$(document).ready(function() {
    window.g_index = 0;
    
    $(function(){
        window.g_index = $("[latest_index]").attr('latest_index');
        $("[index=" + window.g_index + "]").css("color","red");
    });

    

    $(".btn-default").click(function() {
        if(window.g_index != 0){
            $("[index=" + window.g_index + "]").css("color","");
        }
        $(this).css("color","red");
        window.g_index = $(this).attr("index");
        return false;
    });
    
    $("#update_follow").click(function(){
        var index = window.g_index;
        e = index % 100;
        s = (index - e) / 100;
        data = {
            "latest_season" : s,
            "latest_episode" : e
        }

        $.post(window.location.pathname,data);


    });

});
