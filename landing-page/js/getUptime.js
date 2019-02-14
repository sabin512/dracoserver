
function buildXhttp() {
    if (window.XMLHttpRequest) {
        xhttp = new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        xhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xhttp;
}

function getUptime()  {
    var xhttp = buildXhttp();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
           var jsonData = JSON.parse(xhttp.responseText);
           document.getElementById("uptimeSlot").innerHTML = jsonData.uptime + "&nbsp;(hh:mm:ss)";
           document.getElementById("tempSlot").innerHTML = jsonData.temperature + "&deg;";
           document.getElementById("hmdSlot").innerHTML = jsonData.humidity + "%";
           document.getElementById("counterSlot").innerHTML = jsonData.counter + "&nbsp;times";
           document.getElementById("lci1Slot").innerHTML = jsonData.lci1;
           document.getElementById("lci2Slot").innerHTML = jsonData.lci2;
           document.getElementById("readingCountSlot").innerHTML = jsonData.readingCount;
        }
    }
    xhttp.open("GET", "http://iotowl.duckdns.org/dracoserver/dracocollector/getLiveData?sourceName=Lyra", true);
    xhttp.send();

}

/*var status = function(){
	if (
	$('.status').addClass('.status-online').text('online');
	$('.status').addClass('.status-offline').text('offline');

};
$(window).ready(status); */
window.setInterval(getUptime, 5000);
