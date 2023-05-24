const apiKey = document.getElementById("api-key").innerHTML;

// Initialize and add the map
(g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})
  ({
    key: apiKey,
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

  const stationMarkers = await showStations().then();
  // console.log(stationMarkers);
  // let button = document.getElementById("clear_markers");
  // button.addEventListener("click", function() {clearMarkers(stationMarkers);});
} 

var clearMarkers = (markers) => {
  var marker;
  for (index in markers){
    marker = markers[index];
    marker.setMap(null);
  }
}

async function showStations(){
  const response = await fetch('../static/data/stations.json');
  const stations_data = await response.json();
  var allStationMarkers = new Array();
  let marker_promise;
  for (index in stations_data) {
    const station = stations_data[index];
    const lat = station[2];
    const lng = station[3];
    const name = station[1];
    const id = station[0];
    const info = name + '<br>id: '+id
    marker_promise = makeMarker(map, lat, lng, info, id);
    allStationMarkers.push(marker_promise);
  }
  return allStationMarkers;
}

//makes a marker on the map given map, coords, and a string for some info
var makeMarker = (map, lat1, lng1, info, id) => {
  const arr = info.split('id: ');
  const infowindow = new google.maps.InfoWindow({
    content: '<div id="marker"><h6>' + arr[0] + '</h6><p>Station ID: ' + arr[1] + '</p></div>',
    ariaLabel: "Times New Roman",
  });
  const marker = new google.maps.Marker({
    position: { lat: lat1, lng: lng1 },
    map,
    title: ""+id,
    icon: "../static/blue-icon.png",
  });

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

// let button_map = document.getElementById("button_map");
// let button = document.getElementById("submit");
// button_map.addEventListener("click", initMap);
window.initMap = initMap;
initMap()