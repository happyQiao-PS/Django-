$(function () {
    $(".ischose").click(function () {
        $that = $(this);
        $cartid = $that.parent().parent().attr("cartid");
        $.ajax({
            url: "/axf/selected/",
            type: "get",
            data: {
                "cartid": $cartid,
            },
            success: function (data) {
                if (data["key"]) {
                    $that.find("span").text("√");
                    if (data["select_all"]){
                        $(".confirm").find("span").find("span").html("√");
                    }
                } else {
                    $that.find("span").text("");
                    if (!data["select_all"]){
                        $(".allSelect").html("");
                    }
                }
                $(".price").html(data["s_price"]);
            }
        });
    });

    sub_or_add_cart();

    $(".selectAll").click(function () {
        $select_list = [];
        $unselect_list = [];
        $select_all = $(this);
        $(".menuList>div>span>span").each(function () {
            $menu_list = $(this);
            $cartid = $menu_list.parents("li").attr("cartid");
            if ($menu_list.html().trim() === "√") {
                $select_list.push($cartid);
            } else {
                $unselect_list.push($cartid);
            }
        });
        /*判断逻辑
        * 判断是否存在没被选中的元素，如果存在就吧没选中的发给后端把他变成选中的状态
        * */
        if ($unselect_list.length > 0) {
            $.ajax({
                url:"/axf/selectall/",
                type:"get",
                data:{
                    "unselect_list":$unselect_list.join("#"),
                },
                success:function (data) {
                    if(data["statu"]==="good"){
                        $(".confirm").find("span").find("span").html("√");
                    }
                    $(".price").html(data["s_price"]);
                },
                fail:function () {
                    console.log("error");
                }
            });
        }else if ($unselect_list.length === 0) {
            $.ajax({
                url:"/axf/selectall/",
                type:"get",
                data:{
                    "unselect_list":$select_list.join("#"),
                },
                success:function (data) {
                    if(data["statu"]==="good"){
                        $(".confirm").find("span").find("span").html("");
                    }
                    $(".price").html(data["s_price"]);
                },
                fail:function () {
                    console.log("error");
                }
            });
        }
    });
});

/*加减法逻辑*/
function sub_or_add_cart() {
    /*加法*/
    $(".addShopping").click(function () {
        $that = $(this);
        $cartid = $that.parent().parent().attr("cartid");
        if ($cartid) {
            $.ajax({
                url: "/axf/change_cart_num/",
                type: "post",
                data: {
                    "key": "+",
                    "cartid": $cartid
                },
                success: function (data) {
                    switch (data["login-statu"]) {
                        case "Not Login":
                            window.open("/axf/login/", "_self");
                            break;
                        case "Login OK":
                            $num = data["choice_num"];
                            buy_num($that, $num, "+");
                    }
                    $(".price").html(data["s_price"]);
                }

            })
        }
    });
    /*减法*/
    $(".subShopping").click(function () {
        $that = $(this);
        $cartid = $that.parent().parent().attr("cartid");
        if ($cartid) {
            $.ajax({
                url: "/axf/change_cart_num/",
                type: "post",
                data: {
                    "key": "-",
                    "cartid": $cartid
                },
                success: function (data) {
                    switch (data["login-statu"]) {
                        case "Not Login":
                            window.open("/axf/login/", "_self");
                            break;
                        case "Login OK":
                            $num = data["choice_num"];
                            buy_num($that, $num, "-");
                    }
                    $(".price").html(data["s_price"]);

                }

            })
        }
    })
}

function buy_num($that, $num, flag) {
    if (flag === "+") {
        $span = $that.prev("span").text($num);
    } else if (flag === "-") {
        if ($num > 0) {
            $span = $that.next("span").text($num);
        } else if ($num === 0) {
            $span = $that.parents("li").hide();
        }
    }
}
