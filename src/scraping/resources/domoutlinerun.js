
window.selected_elements = []
window.selection_finished = false
var myExampleClickHandler = function (element) {
    console.log('Clicked element:', element);
    window.selected_elements = window.selected_elements.concat(element)
    console.log('SelectedElements:', window.selected_elements);
    window.myDomOutline.start()
}
window.myDomOutline = Domoutlinelib({ onClick: myExampleClickHandler, filter: '*' });

// Start outline:
window.myDomOutline.start();

window.addEventListener("keydown", function (event) {
    console.log(event.key);
  switch (event.key) {

    case "ArrowRight":
        console.log("finished!!!!!")
        window.myDomOutline.stop();
      window.selection_finished = true
      break;
    default:
      return; // Quit when this doesn't handle the key event.
  }

  // Cancel the default action to avoid it being handled twice
  event.preventDefault();
}, true);