
let map;
const mapsKey = process.env.GMAPS_KEY

const initMap = () => {
  console.error("Je suis activé !");
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    zoom: 8
  });
}

fetch("https://maps.googleapis.com/maps/api/js?key=mapsKey&callback=initMap")

