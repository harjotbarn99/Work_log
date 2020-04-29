

function setUserWel(){
 getKey();
 document.getElementById("welcome").innerHTML = "Welcome " + user;
};

function getEle(i) {
    return document.getElementById(i)

}

function sendDetails(){
    let TypeOfWork;
    let fieldWork = getEle("Fieldwork");
    let officeW= getEle("Office");
    if(fieldWork.checked){
        TypeOfWork = fieldWork.value;
    };
    if(officeW.checked){
        TypeOfWork = officeW.value;
    }

    let description = getValAndClear('description');
    let toSend = {'typeOfWork':TypeOfWork,'description':description};
    console.log(toSend)
    let toSendJson = JSON.stringify(toSend);
    encryptedAjaxPostRequest("/addWork",toSendJson,message);
}

function message(dataJ){
    let dic = JSON.parse(dataJ);
    document.getElementById('message').innerHTML=dic.message;
}

function logs(){
    window.location.replace("/logs.html")
}

