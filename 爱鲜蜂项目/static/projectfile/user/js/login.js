$(function () {

});

function check_login() {
    $username = $("#username_info");
    $password = $("#password_input");
    if (($username.val().trim()).length>0 && ($password.val().trim()).length>0){
        $password.val(md5($password.val().trim()));
        return true;
    }
    else{
        $(".login-status").show();
    }
    return false;
}