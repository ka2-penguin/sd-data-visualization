// Initialize and add the map
(g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})
  ({
    key: "AIzaSyBm90rp3Nys_NhgCMY5zRTTMTTLbaPzeZs",
    // Add other bootstrap parameters as needed, using camel case.
    // Use the 'v' parameter to indicate the version to load (alpha, beta, weekly, etc.)
  });  

let map;
async function initMap(data) {
  const { Map } = await google.maps.importLibrary("maps");
  const center = { lat: 40.730610, lng: -73.935242 }; // centered on NYC
  const radius = .5;
  const zoom = 11;

  map = new Map(document.getElementById("map"), {
    center: center,
    zoom: zoom,
    minZoom: zoom - 2,
    maxZoom: zoom + 4,
    restriction: {
      latLngBounds: {
        north: center["lat"] + radius,
        south: center["lat"] - radius,
        east: center["lng"] + radius,
        west: center["lng"] - radius,
      },
    },
  });

  const directionsService = new google.maps.DirectionsService();
  const directionsRenderer = new google.maps.DirectionsRenderer({
    draggable: false,
    map,
    panel: document.getElementById("map"),
  });

  var result = document.getElementById("results").value.split(",")

  displayRoute(
    // Replace with two stations later 
    // { lat: 40.717805, lng: -74.014072 }, 
    // { lat: 40.708455, lng: -73.999741 },
    {lat: result[0], lng: result[1]},
    {lat: result[2], lng: result[3]},
    directionsService,
    directionsRenderer
  );

  const stationMarkers = await showStations().then();
  console.log(stationMarkers);
  let button = document.getElementById("clear_markers");
  button.addEventListener("click", function() {clearMarkers(stationMarkers);});
} 

function displayRoute(origin, destination, service, display) {
  service
    .route({
      origin: origin,
      destination: destination,
      travelMode: google.maps.TravelMode.BICYCLING,
    })
    .then((result) => {
      display.setDirections(result);
    })
    .catch((e) => {
      alert("Could not display directions due to: " + e);
    });
}

function computeTotalDistance(result) {
  let total = 0;
  const myroute = result.routes[0];

  if (!myroute) {
    return;
  }

  for (let i = 0; i < myroute.legs.length; i++) {
    total += myroute.legs[i].distance.value;
  }

  total = total / 1000;
  document.getElementById("total").innerHTML = total + " km";
}

let button_map = document.getElementById("button_map");
let button = document.getElementById("submit");
button_map.addEventListener("click", initMap);
window.initMap = initMap;
initMap()