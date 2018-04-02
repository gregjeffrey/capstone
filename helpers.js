function updateLocation(loc) {
    localStorage.setItem("goatsFarmLocation", loc);
}
function getLocation() {
	var loc = localStorage.getItem("goatsFarmLocation");
	return loc;
}