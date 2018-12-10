$(document).ready(function() {

    // Ask user if they really want to complete order.
    $('.update_status').submit(function() {
        let answer = confirm('Do you want to update the status?')
        if (answer)
        {
            return true;
        } else {
            return false;
        }
    })

});