var c = document.getElementById("playground");
var ctx = c.getContext("2d");
var bike_data;
var max_height;

var width = c.getBoundingClientRect().width;
var height = c.getBoundingClientRect().height;

var resize = (e) =>{
	console.log(window.innerWidth);
	console.log(window.innerHeight);
	ctx.canvas.height = window.innerHeight;
	ctx.canvas.width  = window.innerWidth;
	
	width = c.getBoundingClientRect().width;
	height = c.getBoundingClientRect().height;
}
resize()

window.addEventListener("resize", () => {
	resize();
	redraw("Citibike Trips per Month", "Month", "Trips",bike_data,max_height)
})
const months = [
	"January",
	"February",
	"March",
	"April",
	"May",
	"June",
	"July",
	"August",
	"September",
	"October",
	"November",
	"December",
]

// var data = new Array();

async function getData(){
	const response = await fetch('../static/data/monthly_data.json');
	const monthly_data = await response.json();
	// console.log(monthly_data)
	var new_data = [];
	for (index in monthly_data) {
		const month = months[index];
		const month_data = monthly_data[index];
		const new_data_point = [month, month_data[0], month_data[1]];
		new_data.push(new_data_point);
	}

	var max = 0;
	for (const i of new_data){
		if (i[1] > max) max = i[1];
	}
	redraw("Citibike Trips per Month", "Month", "Trips", new_data, max)
}
getData();
// getData(data);
// const data = getData();
// console.log(data);

// // const data = [["January", 30,10], ["February", 50,42], ["March", 120,63], ["April", 80,10],["January", 30,10]]
// var max = 0;
// for (const i of data){
// 	if (i[1] > max) max = i[1];
// }

var redraw = (title, labelX, labelY, data, max) => {
	bike_data = data;
	max_height = max;
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = 'rgba(255,255,255,1)';
    ctx.fillRect(0,0, width, height);

    //title + labels
    ctx.fillStyle = 'rgb(10,10,10)';
    ctx.textRendering = "optimizeLegibility";
    ctx.font = (width / 20) + "px Arial";
    ctx.textAlign = "center";
    ctx.fillText(title, ctx.canvas.width/2, 5 * height/40);
    ctx.font = (width / 30) + "px Arial";
    ctx.fillText(labelX, ctx.canvas.width/2, 37 * height/40);

    ctx.save();
	ctx.translate(0, height);
	ctx.rotate(-Math.PI/2);
	ctx.textAlign = "center";
	ctx.fillText(labelY, 1.11 * height/2,width/20);
	ctx.restore();

    //axes
    ctx.beginPath();
	ctx.moveTo(5*width/48, height/6);
	ctx.lineTo(5*width/48, 3 * height / 4);
	ctx.lineTo(11 * width/12, 3 * height / 4);
	ctx.stroke();
	ctx.closePath();

	//data
	//x dimensions: 3width/24 to 21width/24
	//y dimensions: height/4 to 3height/4
	const boxWidth = (3*width/4) / data.length;
	const maxBoxHeight = height / 2;

	ctx.beginPath();
	ctx.moveTo(5*width/48, 3*height/4 - maxBoxHeight);
	ctx.lineTo(5*width/48 - width/96, 3*height/4 - maxBoxHeight);
	ctx.stroke();
	ctx.closePath();
	ctx.font = (width / 60) + "px Arial";
	ctx.fillText(max, 5*width/48 - 5*width/110, 73*height/96 - maxBoxHeight);

	for (var i = 0; i < data.length; i++){
		ctx.fillStyle = 'rgba(255,0,0,1)';
		ctx.fillRect(boxWidth * i + width/8,3 * height / 4 - ((data[i][1] / max) * maxBoxHeight), boxWidth, (data[i][1] / max) * maxBoxHeight);
		ctx.fillStyle = 'rgba(0,0,255,0.4)';
		ctx.fillRect(boxWidth * i + width/8,3 * height / 4 - ((data[i][2] / max) * maxBoxHeight), boxWidth, (data[i][2] / max) * maxBoxHeight);
		ctx.fillStyle = 'rgb(10,10,10)';
		ctx.font = (width / 80) + "px Arial";
		ctx.fillText(data[i][0], boxWidth * (i + 0.5) + width/8,19 * height / 24);
	}
};

// redraw("Chart", "Month", "CitiBikes Used", data)