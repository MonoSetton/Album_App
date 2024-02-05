$(document).ready(function () {
    // Submit comment form via AJAX
    $('form.comment-form').submit(function (event) {
        event.preventDefault();

        var form = $(this);
        var formData = new FormData(form[0]);
        var sectionId = form.data('section-id');  // Retrieve the section ID

        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
                // Append the new comment to the correct comments section
                var commentHtml = '<div id="comment-' + data.id + '" class="comment">' +
                    '<span class="comment-author">' + data.author + '</span>' +
                    '<p class="comment-body">' + data.body + '</p>';
                    console.log(data, data.id)
                    commentHtml += '<form class="delete-comment-form" action="/delete_comment/0'.replace('0', data.id) + '" method="post">' +
                        '<button type="submit" class="btn btn-danger btn-sm delete-comment">Delete</button>' +
                        '</form>';


                // Close the comment div
                commentHtml += '</div>';
                $('#comments-section-' + sectionId).append(commentHtml);

                // Clear the form after successful submission
                form.trigger('reset');
            },
            error: function (error) {
                console.error('Error submitting comment:', error);
            }
        });
    });


    function getCSRFToken() {
        var csrfToken = null;
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.startsWith('csrftoken=')) {
                csrfToken = cookie.substring('csrftoken='.length, cookie.length);
                break;
            }
        }
        return csrfToken;
}


    // Delete comment via AJAX
    $(document).on('submit', '.delete-comment-form', function (event) {
        event.preventDefault();

        var form = $(this);
        var commentId = form.attr('action').split('/').pop(); // Extract comment ID from the form action URL
        var csrfToken = getCSRFToken(); // Get the CSRF token from the cookie

        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: {'comment_id': commentId},
            headers: {'X-CSRFToken': csrfToken},  // Include the CSRF token in the request headers
            success: function () {
                // Remove the deleted comment from the comments section
                $('#comment-' + commentId).remove();
            },
            error: function (error) {
                console.error('Error deleting comment:', error);
            }
        });
    });
});