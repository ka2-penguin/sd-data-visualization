var c = document.getElementById("playground");
var ctx = c.getContext("2d");

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
	redraw("Chart", "Month", "CitiBikes Used")
})

const data = [["January", 30], ["February", 50], ["March", 120], ["April", 80],["January", 30], ["February", 50], ["March", 120], ["April", 80]]
var max = 0;
for (const i of data){
	if (i[1] > max) max = i[1];
}

var redraw = (title, labelX, labelY, arr) => {
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

	//data
	//x dimensions: 3width/24 to 21width/24
	//y dimensions: height/4 to 3height/4
	const boxWidth = (3*width/4) / data.length;
	const maxBoxHeight = height / 2;

	for (var i = 0; i < data.length; i++){
		ctx.fillStyle = 'rgba(255,0,0,1)';
		ctx.fillRect(boxWidth * i + width/8,3 * height / 4 - ((data[i][1] / max) * maxBoxHeight), boxWidth, (data[i][1] / max) * maxBoxHeight);
		ctx.fillStyle = 'rgb(10,10,10)';
		ctx.font = (width / 60) + "px Arial";
		ctx.fillText(data[i][0], boxWidth * (i + 0.5) + width/8,19 * height / 24);
	}
};

redraw("Chart", "Month", "CitiBikes Used", data)