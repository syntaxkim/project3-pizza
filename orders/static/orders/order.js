$(document).ready(function() {

    // Make sure all information is correct before request to server
    $("#next").submit(function() {

        if (!$("#next input[name=user_id]").val())
        {
            alert("Bad request.");
            return false;
        }
        else if (!$("#next input[name=contact]").val())
        {
            alert("Missing contact information.");
            return false;
        }
        else if (!$("#next input[name=billing_address]").val())
        {
            alert("Missing billing address.");
            return false;
        }
        else if (!$("#next input[name=shipping_address]").val())
        {
            alert("Missing shipping address.");
            return false;
        }
        return true;
    });
    
    $('#order').submit(function() {
        let answer = confirm('Do you want to place an order?')
        if (answer)
        {
            return true;
        } else {
            return false;
        }
    })

});