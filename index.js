var data = document.getElementById('data');

var start = new Date().getTime(); // Start time

setInterval(function() {
	//Calculating the current second
	var current_second = Math.floor((new Date().getTime() - start)/1000);
	
	var str_data = httpGet('/api/data');
	var formatted_data = JSON.parse(str_data);
	
	data.innerHTML += current_second + " : " + "Speed : " + Math.floor(formatted_data.speed.val) + " " + formatted_data.speed.unit + "<br><hr>";
	
	console.log(formatted_data);
}, 1000); // Performs the request every 1 seconds


// This function performs GET request and returns response as String
function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}