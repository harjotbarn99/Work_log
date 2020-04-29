function today() {
    setUserWel();
    ajaxGetRequest("/logsToday",displayToday)
}

function displayToday(liOfLiJ) {
    liOfLi = JSON.parse(liOfLiJ);
    let Final = "";
    for (let li of liOfLi){
        let Sli = li.toString(li);
        Final = Final + Sli + "<br>"
    }
    document.getElementById("today").innerHTML = Final;
}


function custom() {
 let date = document.getElementById('Cdate').value;
 let tosend = JSON.stringify(date);
 encryptedAjaxPostRequest("/logsSpecific",tosend,dispCust);
}


function dispCust(dataJ) {
    let liOfLi = JSON.parse(dataJ);
    let Final = "";
    for (let li of liOfLi){
        let Slili = li.toString(li);
        Final = Final + Slili + "<br>"
    }
    document.getElementById("custom").innerHTML = Final
}