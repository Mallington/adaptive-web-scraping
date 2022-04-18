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

window.make_elements_red_within = function (x1, y1, x2, y2) {
    var elements = window.rectangleSelect("*", x1, y1, x2, y2);
    window.make_elements_red(elements);
}