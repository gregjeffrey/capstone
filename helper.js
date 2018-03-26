var l = 0;
function updateLocation(loc) {
    alert("current sotred loc: " + l);
    alert("new desired loc: " + loc);
	l = loc;
	alert("helpers.js stored loc: " + window.l)
}
function getLocation() {
	return window.l;
}