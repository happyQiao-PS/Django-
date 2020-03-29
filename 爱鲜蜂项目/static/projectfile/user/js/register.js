$(function () {
    check_username();
    check_email();
    check_password();
});


function check_password() {
    $("#password_input_2").change(function () {
        $password_1 = $(this).val().trim();
        $password_2 = $("#password_input_1").val().trim();
        if ($password_1===$password_2){
            $("#password_OK").show();
            $("#password_NO").hide();
        }else{
            $("#password_NO").show();
            $("#password_OK").hide();
        }
    });
}

/*
*
* 注意：
* 200代表这个数据不存在与数据库，也就是可以使用的意思千万不要误解
* 404才是这个数据已经存在的意思
* */
function check_email() {
    $("#email_input").change(function () {
        $email = $(this).val().trim();
        if ($email.length>0){
            $.getJSON(
                "/axf/register_check_email/",
                {"email":$email},
                function (data) {
                    switch (data["data"]){
                        case "200":useremail_OK();
                            break;
                        case "404":useremail_NO();
                            break;
                    }
                }
            );
        }
    });
}
function useremail_OK(){
    $(".email_OK").show();
    $(".email_NO").hide();
}
function useremail_NO() {
    $(".email_NO").show();
    $(".email_OK").hide();
}


function  check_username() {
    $("#username_input").change(function () {
        $username = $(this).val().trim();
        if ($username.length>0){
            $.getJSON(
                "/axf/register_check_username/",
                {"username":$username},
                function (data) {
                    switch (data["data"]){
                        case "200":username_OK();
                            break;
                        case "404":username_NO();
                            break;
                    }
                }
            );
        }
    });
}

function username_OK() {
    $(".username_OK").show();
    $(".username_NO").hide();
}

function username_NO() {
    $(".username_NO").show();
    $(".username_OK").hide();
}

function check() {
    $("#password_input_2").val(md5($("#password_input_2").val().trim()));
    if ($(".username_NO").is(":visible") || $("#password_NO").is(":visible") || $(".email_NO").is(":visible")
        || $("#username_input").val().trim().length===0
        || $("#password_input_1").val().trim().length===0
        || $("#password_input_2").val().trim().length===0
        || $("#email_input").val().trim().length===0
        || $("#img_file_input").val().trim().length===0
    ) {
        return false;
    }
    return true;
}