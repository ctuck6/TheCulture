function likeFunction(button) {
    if (button.className == "review-icon fa fa-heart w3-hover-opacity") {
        button.className = "review-icon fa fa-heart-o w3-hover-opacity";
    } else {
        button.className = "review-icon fa fa-heart w3-hover-opacity";
    }
}

function myFunction() {
    var view = document.getElementById("navbar");
    if (view.className === "navbar") {
        view.className = "overlay";
        view.id = "overlay";
        openNav();
    }
}

function openNav() {
    var view = document.getElementById("overlay");
    var content = document.getElementById("content_overlay");
    content.className = "overlay-content"
    view.style.width = "100%";
    document.getElementById("closebtn").style.display = "block";
}

function closeNav() {
    var view = document.getElementById("overlay");
    view.className = "navbar";
    view.id = "navbar";
    var content = document.getElementById("content_overlay");
    content.className = ""
    document.getElementById("closebtn").style.display = "none";
}

window.onscroll = function() {
    if (window.pageYOffset == 0) {
        document.getElementById("navbar").style.top = "0";
    } else {
        document.getElementById("navbar").style.top = "-75px";
    }
};

$(document).ready(function() {
    $("#editButton").click(function() {
        $("#usernameField").hide();
        $("#emailField").hide();
        $("#editButton").hide();
    });
    $("#cancelButton").click(function() {
        $("usernameField").show();
        $("emailField").show();
        $("editButton").show();
    });
});
