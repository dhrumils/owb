/**
 * file     login.js
 *          provides backend functions for login page
 * author   Glide Technology Pvt. Ltd. <www.glidemtech.com>
 * version  1.0
 * date     29, Jul, 2017
 */

/*******************************************************************************
* constants
*******************************************************************************/

/*******************************************************************************
* global variables
*******************************************************************************/

/*******************************************************************************
* helper methods
*******************************************************************************/

/*******************************************************************************
* event methods
*******************************************************************************/

function onSigninClicked(){
    var username = document.getElementById("txtUsername").value;
    var password = document.getElementById("txtPassword").value;
    localStorage.setItem("username", username);
    data = {'username':username, 'password':password};
    $.getJSON("/login_verify_credentials", data, onSigninSuccess, onSigninFailed);
}


function onForgotPasswordClicked(){
  $.getJSON("/forgot_password" ,{ } ,onForgotPasswordSuccess , onForgotPasswordFailed);
}

/*******************************************************************************
* success callbacks
*******************************************************************************/

function onSigninSuccess(data){
    if (data['result'] == true){
        window.location.href='gateway.html';
    }
    else {
        $("#txtError").show();
    }
}

function onForgotPasswordSuccess(){
    alert ("Credentials sent to registered mail.");
}
/*******************************************************************************
* error callbacks
*******************************************************************************/

function onSigninFailed(){
    $("#txtError").show();
}

function onForgotPasswordFailed(){
    alert ("Couldn't send Password! Please try again.");
}
