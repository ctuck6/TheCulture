function getCountry(value) {
    if (value == "United States") {
        $("#state-list").show();
    } else {
        $("#state-list").hide();
    }
}

$(document).ready(function() {
    $(".show-button").click(function() {
        $(".collapse-field").hide();
        $(".collapse").show();
    });

    $(".hide-button").click(function() {
        $(".collapse").hide();
        $(".collapse-field").show();
    });

    $(document).on('click', '.updateCommentButton', function() {
        var comment_id = $(this).attr('comment_id');
        var article_id = $(this).attr('article_id');
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
            data : {comment_id : comment_id, article_id : article_id}
        });

        req.done(function(data) {
            $('#comment-section' + comment_id).html(data);
        });
    });

    $(document).on('click', '.saveCommentButton', function() {
        var comment_id = $(this).attr('comment_id');
        var article_id = $(this).attr('article_id');
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
            url : '/comment/save',
            type : 'POST',
            data : {comment_id : comment_id, article_id : article_id, body : new_body}
        });

        req.done(function(data) {
            $('#comment-section' + comment_id).html(data);
        });
    });

    $(document).on('click', '.updateReviewButton', function() {
        var review_id = $(this).attr('review_id');
        var product_id = $(this).attr('product_id');
        var csrftoken = $('meta[name=csrf-token]').attr('content')

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        req = $.ajax({
            url : '/review/update',
            type : 'POST',
            data : {review_id : review_id, product_id : product_id}
        });

        req.done(function(data) {
            $('#review-section' + review_id).html(data);
        });
    });

    $(document).on('click', '.saveReviewButton', function() {
        var review_id = $(this).attr('review_id');
        var product_id = $(this).attr('product_id');
        var new_body = $('#review_input' + review_id).val();
        var csrftoken = $('meta[name=csrf-token]').attr('content')

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        req = $.ajax({
            url : '/review/save',
            type : 'POST',
            data : {review_id : review_id, product_id : product_id, body : new_body}
        });

        req.done(function(data) {
            $('#review-section' + review_id).html(data);
        });
    });
});


$(".phoneNumber").keypress(function(event) {
    if (event.which < 47 || event.which > 57) {
        event.preventDefault();
    }
});
