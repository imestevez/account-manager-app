function today() {
    return Date()
}

/* Function used to validate all fields*/
function validate(id) {
    var toret = false;
    var elements = document.getElementById(id).elements;
    var length = elements.length;
    var element;

    for (var i = 0; i < length; i++) {
        element = elements[i];
        if ((element.type === "text") || (element.type === "textarea")) {
            toret = validate_text(element);
        }
        if (element.type === "number") {
            toret = validate_number(element);
        }
    }
    return toret;
}

/* Function used to valiedate text fields*/
function validate_text(field) {
    var toret = false;
    var element = document.getElementById(field.id);
    var expr = /^[a-zA-ZáéíóúÁÉÍÓÚ ,@€%"¡!¿?'._\-\s]+$/;

    var varDivError = "div_".concat(element.id);
    if (element.value === "") {
        element.setCustomValidity("El campo es obligatorio");
        showEmptyError(varDivError);
        toret = false;
    } else {
        if (!expr.test(element.value)) {
            element.setCustomValidity("Formato incorrecto");
            showFormatError(varDivError);
            toret = false;
        } else {
            hideError(varDivError);
            element.setCustomValidity("");
            toret = true;
        }
    }
    return toret;
}

/* Function used to valiedate number fields*/
function validate_number(field) {
    var toret = false;
    var element = document.getElementById(field.id);
    var expr = /^[0-9]+[,.]?[0-9]*$/;
    var varDivError = "div_".concat(element.id);
    if (element.value === "") {
        element.setCustomValidity("El campo es obligatorio");
        showEmptyError(varDivError);
        toret = false;
    } else {
        if (expr.test(element.value)) {
            if (element.value === "0") {
                element.setCustomValidity("Importe mayor que 0.");
                showZeroError(varDivError);
                toret = false;
            } else {
                hideError(varDivError);
                element.setCustomValidity("");
                toret = true;
            }
        } else {
            element.setCustomValidity("Sólo números positivos.");
            showNumberError(varDivError);
            toret = false;
        }
    }
    return toret;
}

function showEmptyError(id) {
    var divErr = document.getElementById(id);
    divErr.innerHTML = "El campo es obligatorio";
    divErr.style.display = "block";
}

function showFormatError(id) {
    var divErr = document.getElementById(id);
    divErr.innerHTML = "Formato incorrecto. Solamente se aceptan letras, comas puntos y guiones.";
    divErr.style.display = "block";
}

function showZeroError(id) {
    var divErr = document.getElementById(id);
    divErr.innerHTML = "El valor del importe no puede ser 0.";
    divErr.style.display = "block";
}

function showNumberError(id) {
    var divErr = document.getElementById(id);
    divErr.innerHTML = "Solo se aceptan números positivos.";
    divErr.style.display = "block";
}

function hideError(id) {
    var divErr = document.getElementById(id);
    divErr.innerHTML = "";
    divErr.style.display = "none";
}

