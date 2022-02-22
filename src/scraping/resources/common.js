
window.getDefaultStyling = function(tagName){
    if(!tagName) tagName = "dummy-tag-name";



    var iframe = document.createElement("iframe");

    document.body.appendChild(iframe);



    var iframeDocument = iframe.contentDocument;
    var targetElement = iframeDocument.createElement(tagName);

    iframeDocument.body.appendChild(targetElement);



    var styling = iframe.contentWindow.getComputedStyle(targetElement);
    var clonedStyling = {};

    for(var i = 0, len = styling.length; i < len; i++){
        var property = styling[i];

        clonedStyling[i] = property;
        clonedStyling[property] = styling[property];
    }



    document.body.removeChild(iframe);



    return clonedStyling;
};

window.getUniqueUserStyling = function(element){
    var allStyling = window.getComputedStyle(element);
    var defaultStyling = window.getDefaultStyling(element.tagName);

    var userStyling = {};

    for(var i = 0, len = allStyling.length; i < len; i++){
        var property = allStyling[i];
        var value = allStyling[property];
        var defaultValue = defaultStyling[property];

        if(value != defaultValue){
            userStyling[property] = value;
        }
    }

    return userStyling;
};

window.getStyleAsString = function(style){
    append = ""
    Object.keys(style).forEach(function(key,index) {
    append += key + ":"+style[key]+ "; "
    });
    return append;
};

window.insertStyleProperty  = function(element){
    unique_style = window.getUniqueUserStyling(element)
    unique_style_string = window.getStyleAsString(unique_style)
    element.style = unique_style_string
};

window.insertStyleForAllElementsIn  = function(element){
    var all = element.getElementsByTagName("*");

    for (var i=0, max=all.length; i < max; i++) {
            window.insertStyleProperty(all[i]);
            console.log("processing" +i);
    }

};
