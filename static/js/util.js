

//Geolocalizacion

window.onload = function() {getLocation()};

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    let lat = position.coords.latitude;
    let long = position.coords.longitude;
    $("input[name='latitude']").val(lat);
    $("input[name='longitude']").val(long);
}


//Select

$(document).ready(function () {
    $('select').formSelect();
});


//Dropdown
$(document).ready(function () {
    $('.dropdown-trigger').dropdown();
});
//Sidenav

$(document).ready(function () {
    $('.sidenav').sidenav();
});

//Modal

$(document).ready(function () {
    $('.modal').modal();
});

(function () {
    document.getElementById("id_picture").onchange = function () {
        var files = document.getElementById("id_picture").files;
        var file = files[0];
        document.getElementById("info").innerHTML = file.name;
        if (file.size > 5000000) {
            return alert("Archivo demasido grande. No puede sobrepasar los cinco MiB.");
        }
    };
})();

