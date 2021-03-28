let w = $(window).width();
let h = $(window).height();

let hue = 0;
let mouseXpercentage;
let mouseYpercentage;

$(".growable").hover(() => {
    $(this).removeClass("big");
}); 

$(document).mousemove(function(event) {
    mouseXpercentage = Math.round(event.pageX / w * 100);
    mouseYpercentage = Math.round(event.pageY / h * 100);
    
    // var innerColor = "hsl(0, 88%, 51%)";
    // var outerColor = "hsl(0, 77%, 15%)";
    updateBackground();
});

setInterval(() => {
    hue = (++hue) % 360;
    //console.log(hue, mouseXpercentage, mouseYpercentage);
    updateBackground();
}, 50);

function updateBackground() {
    $('.background').css('background', 'radial-gradient(circle at ' + mouseXpercentage + '% ' 
    + mouseYpercentage + '%, hsl(' + hue + ', 88%, 51%), hsl(' + ((hue + 240) % 360) + ', 100%, 20%)');
}

