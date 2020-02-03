var data = document.getElementById('data');

var start = new Date().getTime(); // Current time

setInterval(function() {
	var current_second = Math.floor((new Date().getTime() - start)/1000);
	data.innerHTML += current_second + " : " + httpGet('/api/data') + "<br>";
}, 1000); // Performs the request every 1 seconds


// This function performs GET request and returns response as String
function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}