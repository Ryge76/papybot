// function that creates a <div> element to hold a map
const createMapElt = () => {
  console.log("Creation de l'élément html contenant la carte.");
  let mapElt = document.createElement("div");
  mapElt.classList.add("map");
  console.log("Creation de l'élément html achevée.");
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

// function creating map inside a div element with class 'map'
// Require an Object with coordinates lng/lat.
const createMap = (queryCoord) => {
  console.log("Creation de carte.");
  let elt = createMapElt();
  let map = new google.maps.Map(elt, { center: queryCoord, zoom: 15});
  let marker = new google.maps.Marker({position: queryCoord, map: map})
  console.log("Creation de carte achevée.");
  return elt
}

// function to pass query to Google Maps API and eventually retrieve an address
// Requiere a string. Return a JS Object with an div elt and a string
const gmapsCall = (query) => {
  const coordinates = getCoordinates(query);
  const mapElt = createMap(coordinates['queryCoord']);
  return {elt:mapElt, address:coordinates['queryAddress']}
}


export {gmapsCall, createMap, getCoordinates}

