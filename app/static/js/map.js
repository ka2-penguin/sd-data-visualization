// Initialize and add the map
(g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})
  ({
    key: "AIzaSyBm90rp3Nys_NhgCMY5zRTTMTTLbaPzeZs",
    // Add other bootstrap parameters as needed, using camel case.
    // Use the 'v' parameter to indicate the version to load (alpha, beta, weekly, etc.)
  });  


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

  makeMarker(map, 40.730610, -73.935242, 'my name is skyler white yo');
  showStations();
} 

async function showStations(){
  const response = await fetch('../static/data/stations.json');
  const stations_data = await response.json();
  console.log(stations_data);
  // const stations_data = JSON.parse(stations);
  for (index in stations_data) {
    const station = stations_data[index];
    // console.log(station);
    const lat = station[2];
    const lng = station[3];
    const name = station[1];
    const id = station[0];
    const info = name + '<br>id: '+id
    // console.log(lat);
    makeMarker(map, lat, lng, info);
  }
  // console.log(index);
}

//makes a marker on the map given map, coords, and a string for some info
var makeMarker = (map, lat1, lng1, info) => {
  const infowindow = new google.maps.InfoWindow({
    content: '<p>' + info + '</p>',
    ariaLabel: "Times New Roman",
  });
  // console.log(lat1);
  const marker = new google.maps.Marker({
    position: { lat: lat1, lng: lng1 },
    map,
    title: "Hello World!",
    icon: "../static/blue-icon.png",
  });

  marker.addListener("click", () => {
    infowindow.open({
      anchor: marker,
      map,
    });
  });
}

// let button_map = document.getElementById("button_map");
// button_map.addEventListener("click", initMap);
let button = document.getElementById("submit");

button_map.addEventListener("click", initMap);
initMap()
// button_map.addEventListener("click", showStations);