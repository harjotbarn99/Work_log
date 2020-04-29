var server_public_key;
function setup(){
    getKey();

}

function getValAndClear(id){
  let value = document.getElementById(id).value;
  document.getElementById(id).value="";
  return value;

}


function register(){
  let username = getValAndClear("username");
  let password = getValAndClear("password");
  let email = getValAndClear('email');
  let phoneNumber = getValAndClear("phoneNumber")
  let data = {"username":username,"password":password,"email":email,"phoneNumber":phoneNumber};
  console.log(data)
  let toSend = JSON.stringify(data);
  encryptedAjaxPostRequest("signUp",toSend,registered);
}

function loginPg(){
window.location.replace("/")
}

function registered(jdata){
  //let message = JSON.parse(jdata);
  console.log(jdata)
  document.getElementById("message").innerHTML = jdata;
}