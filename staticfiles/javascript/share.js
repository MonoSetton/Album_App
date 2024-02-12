function ShareURL(id) {
    var url = window.location.origin + '/image_details/' + id
    navigator.clipboard.writeText(url);
    setTimeout(SuccessMessage, 300)
}
function SuccessMessage(){
    alert("Copied URL")
}
