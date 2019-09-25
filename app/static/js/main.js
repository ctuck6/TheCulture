function getCountry(value) {
    if (value === 'United States') {
        $('#state-list').show();
    } else {
        $('#state-list').hide();
    }
}

function isEmpty(value) {
    if(value === '') {
        document.getElementById('post-comment-button').disabled = true;
    } else {
        document.getElementById('post-comment-button').disabled = false;
    }
}

$(document).ready(function() {
    $('.show-button').click(function() {
        $('.collapse-field').hide();
        $('.collapse').show();
    });

    $('.hide-button').click(function() {
        $('.collapse').hide();
        $('.collapse-field').show();
    });

    $(document).on('click', '#post-comment-button', function() {
        var comment_id = $(this).attr('comment_id');
        var article_id = $(this).attr('article_id');
        var count = $(this).attr('count');
        var comment_body = $('#comment-body').val();
        var csrftoken = $('meta[name=csrf-token]').attr('content')

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });

        req = $.ajax({
            url : '/comment/post',
            type : 'POST',
            data : {comment_id : comment_id, article_id : article_id, comment_body : comment_body, count : count}
        });

        req.done(function(data) {
            $('#comments-section').html(data);
        });
    });

    $(document).on('click', '#delete-comment-button', function() {
        var comment_id = $(this).attr('comment_id');
        var article_id = $(this).attr('article_id');
        var csrftoken = $('meta[name=csrf-token]').attr('content')

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });

        req = $.ajax({
            url : '/comment/delete',
            type : 'POST',
            data : {comment_id : comment_id, article_id : article_id}
        });

        req.done(function(data) {
            $('#comments-section').html(data);
        });
    });

    $(document).on('click', '#load-more-button', function() {
        var count = $(this).attr('count');
        var article_id = $(this).attr('article_id');
        var csrftoken = $('meta[name=csrf-token]').attr('content')

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });

        req = $.ajax({
            url : '/comment/load',
            type : 'POST',
            data : {count : count, article_id : article_id}
        });

        req.done(function(data) {
            $('#comments-section').html(data);
        });
    });

    $(document).on('click', '.update-review-button', function() {
        var review_id = $(this).attr('review_id');
        var product_id = $(this).attr('product_id');
        var csrftoken = $('meta[name=csrf-token]').attr('content')

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
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

    $(document).on('click', '.save-review-button', function() {
        var review_id = $(this).attr('review_id');
        var product_id = $(this).attr('product_id');
        var new_body = $('#review_input' + review_id).val();
        var csrftoken = $('meta[name=csrf-token]').attr('content')

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
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

    $(document).on('click', '#like-button', function() {
        var article_id = $(this).attr('article_id');
        var user_id = $(this).attr('user_id');
        var csrftoken = $('meta[name=csrf-token]').attr('content')

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });

        req = $.ajax({
            url : '/article/like',
            type : 'POST',
            data : {article_id : article_id, user_id : user_id}
        });

        req.done(function(data) {
            $('#like').html(data);
        });
    });

    $(document).on('click', '#unlike-button', function() {
        var article_id = $(this).attr('article_id');
        var like_id = $(this).attr('like_id');
        var csrftoken = $('meta[name=csrf-token]').attr('content')

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });

        req = $.ajax({
            url : '/article/unlike',
            type : 'POST',
            data : {article_id : article_id, like_id : like_id}
        });

        req.done(function(data) {
            $('#like').html(data);
        });
    });
});


$('.phoneNumber').keypress(function(event) {
    if (event.which < 47 || event.which > 57) {
        event.preventDefault();
    }
});
