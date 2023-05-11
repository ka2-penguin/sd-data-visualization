var c = document.getElementById("playground");
var ctx = c.getContext("2d");

var width = c.getBoundingClientRect().width;
var height = c.getBoundingClientRect().height;

var resize = (e) =>{
	ctx.canvas.width  = window.innerWidth - 100;
	ctx.canvas.height = ctx.canvas.width / 3 * 2;
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
    ctx.font = "100px Arial";
    ctx.fillText("Text", 0, 0);
};

redraw()