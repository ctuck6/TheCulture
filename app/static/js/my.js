function likeFunction(button) {
    if (button.className == "article-icon fa fa-heart") {
        button.className = "article-icon fa fa-heart-o";
    } else {
        button.className = "article-icon fa fa-heart";
    }
}

function openOverlay() {
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
    $(".show-button").click(function() {
        $(".collapse-field").hide();
        $(".collapse").show();
    });

    $(".hide-button").click(function() {
        $(".collapse").hide();
        $(".collapse-field").show();
    });

    $(".show-comment-form").click(function() {
        var comment_id = $(this).attr('comment_id');
        $('.collapse-field' + comment_id).hide();
        $('.collapse' + comment_id).show();
    });

    $(".hide-comment-form").click(function() {
        var comment_id = $(this).attr('comment_id');
        $('.collapse' + comment_id).hide();
        $('.collapse-field' + comment_id).show();
    });

    $('.updateCommentButton').click(function() {
        var comment_id = $(this).attr('comment_id');
        var new_body = $('#comment_input' + comment_id).val();
        var csrftoken = $('meta[name=csrf-token]').attr('content')

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        req = $.ajax({
            url : '/comment/update',
            type : 'POST',
            dataType: "json",
            data : { id : comment_id, body : new_body }
        });

        req.done(function(data) {
            $('#comment' + comment_id).text(data.updated_body);
        });
    });
});


$(".phoneNumber").keypress(function(event) {
    if (event.which < 47 || event.which > 57) {
        event.preventDefault();
    }
});
