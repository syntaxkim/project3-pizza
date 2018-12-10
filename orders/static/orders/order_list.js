$(document).ready(function() {

    // Ask user if they really want to complete order.
    $('.recieved').submit(function() {
        let answer = confirm('Have you recieved the product?')
        if (answer)
        {
            return true;
        } else {
            return false;
        }
    })

});