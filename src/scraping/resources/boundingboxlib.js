window.rectangleSelect = function (selector, x1, y1, x2, y2) {
    var elements = [];
    jQuery(selector).each(function () {
        var $this = jQuery(this);
        var offset = $this.offset();
        var x = offset.left;
        var y = offset.top;
        var w = $this.width();
        var h = $this.height();

        if (x >= x1
            && y >= y1
            && x + w <= x2
            && y + h <= y2) {
            // this element fits inside the selection rectangle
            elements.push($this.get(0));
        }
    });
    return elements;
}

window.make_elements_red = function (elements) {
    var itm = elements.length;
    while (itm--) {
        elements[itm].style.background = "rgba(255, 0, 0, 0.2)";
        console.log(elements[itm]);
    }
}

window.drawRectangleOverDocument = function (x1,y1,x2,y2){

    var canvas = document.createElement('canvas'); //Create a canvas element
    //Set canvas width/height
    canvas.style.width='100%';
    canvas.style.height='100%';
    //Set canvas drawing area width/height
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    //Position canvas
    canvas.style.position='absolute';
    canvas.style.left=0;
    canvas.style.top=0;
    canvas.style.zIndex=100000;
    canvas.style.pointerEvents='none'; //Make sure you can click 'through' the canvas
    document.body.appendChild(canvas); //Append canvas to body element
    var context = canvas.getContext('2d');
    //Draw rectangle
    context.rect(x1,y1,x2-x1,y2-y1);
    context.fillStyle = "rgba(255, 0, 0, 0.2)";
    context.fill();
}

window.make_elements_red_within = function (x1, y1, x2, y2) {
    // var elements = window.rectangleSelect("*", x1, y1, x2, y2);
    // window.make_elements_red(elements);
    window.drawRectangleOverDocument(x1, y1, x2, y2);
}