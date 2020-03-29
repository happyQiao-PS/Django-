$(function () {
    displayChildItem();

    sub_or_add_cart();
});
function sub_or_add_cart() {
    /*加法*/
    $(".addShopping").click(function () {
        $goodid = $(this).attr("goodid");
        $that = $(this);
        if ($goodid){
            $.ajax({
                url : "/axf/add_to_shopping_cart/",
                type : "post",
                data : {
                    "key":"+",
                    "goodid": $goodid
                },
                success: function (data) {
                    switch (data["login-statu"]){
                        case "Not Login":
                            window.open("/axf/login/","_self");
                            break;
                        case "Login OK":
                            $num = data["choice_num"];
                            buy_num($that,$num,"+");
                    }
                }

            })
        }
    });
    /*减法*/
    $(".subShopping").click(function () {
        $goodid = $(this).attr("goodid");
        $that = $(this);
        if ($goodid){
            $.ajax({
                url : "/axf/add_to_shopping_cart/",
                type : "post",
                data : {
                    "key":"-",
                    "goodid": $goodid
                },
                success: function (data) {
                    switch (data["login-statu"]){
                        case "Not Login":
                            window.open("/axf/login/","_self");
                            break;
                        case "Login OK":
                            $num = data["choice_num"];
                            buy_num($that,$num,"-");
                    }
                }

            })
        }
    })
}

function buy_num($that,$num,flag) {
    if (flag==="+"){
        $span = $that.prev("span").text($num);
    }else if (flag==="-"){
        $span = $that.next("span").text($num);
    }
}

function displayChildItem(){
    $("#display-child").click(function () {
        $("#type_item").show();
        $("#order_item").hide();
        $("#icon_left").removeClass("glyphicon glyphicon-chevron-down").addClass("glyphicon glyphicon-chevron-up");
    });
    $("#type_item").click(function () {
        $(this).hide();
        $("#icon_left").removeClass("glyphicon glyphicon-chevron-up").addClass("glyphicon glyphicon-chevron-down");
    });
    $("#display-order").click(function () {
        $("#order_item").show();
        $("#type_item").hide();
        $("#icon_right").removeClass("glyphicon glyphicon-chevron-down").addClass("glyphicon glyphicon-chevron-up");
    });
    $("#order_item").click(function () {
        $(this).hide();
        $("#icon_right").removeClass("glyphicon glyphicon-chevron-up").addClass("glyphicon glyphicon-chevron-down");

    })
}