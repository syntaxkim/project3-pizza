$(document).ready(function() {

    // Ask user if they really want to delete the review.
    $('#delete').submit(function() {
        let answer = confirm('Are you sure you want to delete this review?')
        if (answer)
        {
            return true;
        } else {
            return false;
        }
    })

});
