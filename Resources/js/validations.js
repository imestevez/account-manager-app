function today() {
    return Date()
}

function validate(id) {
    var toret = false;
    var elements = document.getElementById(id).elements;
    var length = elements.length;
    var element;
    for (var i = 0; i < length; i++) {
        element = elements[i];
        if (element.type === "text") {
            var varDivError = "div_".concat(element.id);
            if (element.value === "") {
                showEmptyError(varDivError);
                toret = false;
            } else {
                hideError(varDivError);
                toret = true;
            }
        }
    }
    return toret;
}

function showEmptyError(id) {
    var divErr = document.getElementById(id);
    divErr.innerHTML = "El campo es obligatorio";
    divErr.style.background = "red";
    divErr.style.display = "block";
}

function hideError(id) {
    var divErr = document.getElementById(id);
    divErr.innerHTML = "";
    divErr.style.display = "none";
}

function refillTextArea(text, id) {
    var textArea = document.getElementById(id);


}