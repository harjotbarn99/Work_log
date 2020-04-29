// get AJAX
function ajaxGetRequest(path, callback){
    let request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if (this.readyState===4&&this.status ===200){
            callback(this.response);
        }
    };
    request.open("GET", path);
    request.send();
}



function encrypt(message) {
    var encrypted_message = server_public_key.encrypt(message, 'RSA-OAEP');
    encrypted_message = btoa(encrypted_message);
    return encrypted_message;
}


function encryptedAjaxPostRequest(path, data, callback){
    var encryptedData = encrypt(data);
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if (this.readyState === 4 && this.status === 200){
            callback(this.response);
        }
    };
    request.open("POST", path);
    request.send(encryptedData);
}



var server_public_key;

function getUsername(){
    console.log('getusername')
    for(var cookie of document.cookie.split(";")){
        var splits = cookie.trim().split("=");
        if(splits[0].trim() === "username"){
            return splits[1].trim();
        }
    }
    return "guest";
}

function getKey(){
    ajaxGetRequest("key", gotKey);
}

let user = getUsername();

function gotKey(response){
    var content = JSON.parse(response);
    var pk = content['key'];
    server_public_key = forge.pki.publicKeyFromPem(pk);

}

function login(){
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  document.getElementById("username").value =  "";
  document.getElementById("password").value = "";
  let data = {"username":username,"password":password};
  let toSend = JSON.stringify(data);
  encryptedAjaxPostRequest('/login', toSend ,loginAttempt);
}

function loginAttempt(j_data){
  let receieved = JSON.parse(j_data);
  document.getElementById("message").innerHTML=receieved.message;
  if (receieved.authenticated){
    window.location.replace("/dashboard.html")
  }
}


function signUp(){
  window.location.replace("/signUpPage");
}





