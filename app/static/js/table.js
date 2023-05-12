var c = document.getElementById("playground");
var ctx = c.getContext("2d");

var width = c.getBoundingClientRect().width;
var height = c.getBoundingClientRect().height;

var resize = (e) =>{
	ctx.canvas.width  = window.innerWidth - 100;
	ctx.canvas.height = ctx.canvas.width / 2;
	width = c.getBoundingClientRect().width;
	height = c.getBoundingClientRect().height;
}
resize()

window.addEventListener("resize", () => {
	resize();
	redraw();
})

var redraw = (e) => {
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = 'rgba(200,0,0,0.1)';
    ctx.fillRect(0,0, width, height);

    ctx.fillStyle = 'rgb(10,10,10)';
    ctx.font = (width / 20) + "px Arial";
    ctx.textAlign = "center";
    ctx.fillText("Text", ctx.canvas.width/2, 50 + width/20);

    ctx.beginPath();
	ctx.moveTo(20, 20);
	ctx.lineTo(20, 200);
	ctx.stroke();

};

redraw()