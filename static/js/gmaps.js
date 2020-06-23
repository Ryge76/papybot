// create <li> element to be added
const addListElt = (content) => {
  let liElt = document.createElement("li");
  liElt.classList.add("visitor");
  liElt.textContent = content;
  return liElt
}

// function to create a map placeholder
const createMapElt = () => {
  let mapElt = document.createElement("div");
  mapElt.classList.add("map");
  return mapElt
}

// let geocoder
// let map
// function initialize() {
//   geocoder = new google.maps.Geocoder();
//   var latlng = new google.maps.LatLng(-34.397, 150.644);
//   var mapOptions = {
//     zoom: 8,
//     center: latlng
//   }
//   map = new google.maps.Map(document.getElementById('map'), mapOptions);
// }




const getCoordinates = (query) => {
  // initialize geocoder to get coordinates from query
  const geocoder = new google.maps.Geocoder();

  geocoder.geocode( {'address' : query}), function(results, status) {
    if (status === 'OK') {
      const queryAddress = results[0].formatted_address;
      const queryCoord = results[0].geometry.location;
      return {queryAddress, queryCoord}
    }
    else {
      console.error("Echec de l'appel API Google: " + status);
      console.error(results);
    }
    }
  }

// function creating map
const createMap = (queryCoord) => {
  let elt = createMapElt();
  let map = new google.maps.Map(elt, { center: queryCoord, zoom: 8 });
  let marker = new google.maps.Marker({ map: map, position: queryCoord });
  return elt
}



/*
{
 address: string,
 location: LatLng,
 placeId: string,
 bounds: LatLngBounds,
 componentRestrictions: GeocoderComponentRestrictions,
 region: string
}

*/
let map;
let marker;
const mapsKey = process.env.GMAPS_KEY

const initMap = () => {
  console.log("Je suis activé !");
  map = new google.maps.Map(mapElt, {
    center: {lat: -34.397, lng: 150.644},
    zoom: 8
  });
  
  marker = new google.maps.Marker({
    position: lieu,
    map: map
  });
}

fetch("https://maps.googleapis.com/maps/api/js?key=mapsKey&callback=initMap")

