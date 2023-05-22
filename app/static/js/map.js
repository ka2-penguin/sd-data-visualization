// Initialize and add the map
(g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})
  ({
    key: "AIzaSyBm90rp3Nys_NhgCMY5zRTTMTTLbaPzeZs",
    // Add other bootstrap parameters as needed, using camel case.
    // Use the 'v' parameter to indicate the version to load (alpha, beta, weekly, etc.)
  });  

// var allStationMarkers;

let map;
async function initMap(data) {
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const center = { lat: 40.730610, lng: -73.935242 };
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

  // makeMarker(map, 40.730610, -73.935242, 'my name is skyler white yo');
  // var allStationMarkers;
  const stationMarkers = await showStations().then();
  console.log(stationMarkers);
  let button = document.getElementById("clear_markers");
  button.addEventListener("click", function() {clearMarkers(stationMarkers);});
} 

var clearMarkers = (markers) => {
  var marker;
  // console.log(markers);
  for (index in markers){
    marker = markers[index];
    // console.log(marker);
    marker.setMap(null);
  }
}

async function showStations(){
  const response = await fetch('../static/data/stations.json');
  const stations_data = await response.json();
// function showStations(){
  var allStationMarkers = new Array();
//   const response = require('../static/data/stations.json');
  // console.log(response)
  // const stations_data = JSON.parse(response);//response.json();
  // console.log(stations_data);
  // const stations_data = JSON.parse(stations);
  // let marker;
  let marker_promise;
  for (index in stations_data) {
    const station = stations_data[index];
    // console.log(station);
    const lat = station[2];
    const lng = station[3];
    const name = station[1];
    const id = station[0];
    const info = name + '<br>id: '+id
    // console.log(lat);
    marker_promise = makeMarker(map, lat, lng, info, id);
    allStationMarkers.push(marker_promise);
  }
  // console.log(index);
  // console.log(allStationMarkers);
  return allStationMarkers;
}

//makes a marker on the map given map, coords, and a string for some info
var makeMarker = (map, lat1, lng1, info, id) => {
  const arr = info.split('id: ');
  const infowindow = new google.maps.InfoWindow({
    content: '<div id="marker"><h6>' + arr[0] + '</h6><p>Station ID: ' + arr[1] + '</p></div>',
    ariaLabel: "Times New Roman",
  });
  // console.log(lat1);
  const marker = new google.maps.Marker({
    position: { lat: lat1, lng: lng1 },
    map,
    // title: "Hello World!",
    title: ""+id,
    icon: "../static/blue-icon.png",
  });

  // allStationMarkers.push(marker);

  marker.addListener("mousemove", () => {
    infowindow.open({
      anchor: marker,
      map,
    });
  });

  marker.addListener("mouseout", () => {
    infowindow.close({
      anchor: marker,
      map,
    });
  });

  return marker;
}

let button_map = document.getElementById("button_map");
// button_map.addEventListener("click", initMap);
let button = document.getElementById("submit");

button_map.addEventListener("click", initMap);
initMap()
// button_map.addEventListener("click", showStations);