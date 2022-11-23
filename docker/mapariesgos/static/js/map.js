let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 22.767470686050675, lng: -102.59196597852653 },
    zoom: 14,
  });
}

window.initMap = initMap;