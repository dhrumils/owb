/**
* file     user.js
*          provides backend functions for user page
* author   Glide Technology Pvt. Ltd. <www.glidemtech.com>
* version  1.0
* date     31, Jul, 2017
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

function onLoad(){
    document.getElementById("spnSignedinUsername").innerHTML= "Signed in as " + localStorage.getItem("username");
}

function onUserInfoSaveClicked(){
    var username = document.getElementById("spnSignedinUsername").innerHTML;
    var firstname = document.getElementById("txtFirstname").value;
    var lastname = document.getElementById("txtLastname").value;
    var emailid = document.getElementById("txtEmailid").value;
    var data = {'firstname':firstname, 'lastname':lastname, 'emailid':emailid};
    $.getJSON("/user_save_details", data, onUserSaveInfoSuccess , onUserSaveInfoFailed);
}

function onCredentialsSaveClicked(){
    var username = document.getElementById("spnSignedinUsername").innerHTML;
    var currentPassword = document.getElementById('txtCurrentPassword').value;
    var newPassword = document.getElementById('txtNewPassword').value;
    var confirmPassword = document.getElementById('txtConfirmPassword').value;
    var data = {'cuurent_password':currentPassword,'new_password':newPassword};
    if (newPassword == confirmPassword){
        $.getJSON("/user_save_credentials", data, onUserSaveCredentialSuccess, onUserSaveCredentialFailed);
    } else {
        alert("Password confirmation failed!");
    }
}

/*******************************************************************************
* Success callbacks
*******************************************************************************/

function onUserSaveInfoSuccess(data){
    if (data['result'] == true) {
        alert(" User Info saved successfully.");
    }
    else {
        alert("Couldn't save User Info!");
    }
}

function onUserSaveCredentialSuccess(data){
    if (data['result']==true){
        alert("Credentails saved successfully.");
    }
    else {
        alert("Couldn't save credentials!");
    }
}

/*******************************************************************************
* error callbacks
*******************************************************************************/

function onUserSaveInfoFailed(){
    alert("User Info not saved successfully.");
}


function onUserSaveCredentialFailed(){
    alert("Couldn't save credentials!");
}
