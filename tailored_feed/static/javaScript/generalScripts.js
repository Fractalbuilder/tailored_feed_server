// Change string case to Title case. <String>.toTitleCase()
String.prototype.toTitleCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};

// The text element must use the message class
function showMessage (elementId, message, color) {
    const { timer } = rxjs;
    const aTimer = timer(3000);
    console.log("AAAAAAAAAa")
    element = document.getElementById(elementId);
    element.style = "display: block; color: " + color;
    element.innerHTML = message;

    aTimer.subscribe(() => {
        element.innerHTML = "";
        element.style = "display: none";
    });
}
