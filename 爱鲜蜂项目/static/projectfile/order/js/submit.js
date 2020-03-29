$(function () {
    $(".btn").click(function () {
        $orderid = $(this).attr("orderid");
        $.getJSON("/axf/payed/",{"orderid":$orderid},function (data) {
            if(data["msg"]==="OK"){
                window.open("/axf/mine/",target="_self");
            }
        })
    });
});