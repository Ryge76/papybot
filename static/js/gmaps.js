// get api key from environnement
const mapsKey = process.env.GMAPS_KEY

// create <li> element to be added
const createListElt = (content, from) => {
  let liElt = document.createElement("li");

  if (from === 'robot') {
    liElt.classList.add("robot");
  }
  else {
    liElt.classList.add("visitor");
  }
  
  liElt.textContent = content;
  return liElt
}

// include element
const addToChat = (element) => {
  let chatElt = document.getElementById("test");
  chatElt.insertAdjacentElement("afterbegin", element);
}

// function that creates a <div> element to hold a map
const createMapElt = () => {
  let mapElt = document.createElement("div");
  mapElt.classList.add("map");
  return mapElt
}

// function to get the address and the coordinates of the place queried
const getCoordinates = (query) => {
  // initialize geocoder to get coordinates from query
  const geocoder = new google.maps.Geocoder();

  geocoder.geocode({'address' : query}), function(results, status) {
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

// function to pass query to Google Maps API and eventually retrieve an address
// Requiere a string. Return a JS Object with an div elt and a string
const gmapsCall = (query) => {
  const coordinates = getCoordinates(query);
  const mapElt = createMap(coordinates['queryCoord']);
  return {elt:mapElt, address:coordinates['queryAddress']}
}

// faire un appel

// récupérer le texte et l'inclure


// récupérer la carte et l'inclure





fetch("https://maps.googleapis.com/maps/api/js?key=mapsKey&callback=initMap")

export {gmapsCall, mapsKey, createMap, getCoordinates, createMapElt}




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