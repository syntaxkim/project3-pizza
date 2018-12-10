document.addEventListener('DOMContentLoaded', () => {
    get_price();
});

// Get overall price of item and options
function get_price() {
    // Get initial price of item.
    var item_price = parseInt(document.getElementById('price').innerHTML);
    var quantity = 1;
    console.log(item_price);

    // Get extra price if it exists.
    if (!(document.getElementById('extra_price') === null)) {
        var extra_price = parseInt(document.getElementById('extra_price').innerHTML);
        console.log(extra_price);
    };

    // When quantity changed,
    document.querySelector('#quantity').onchange = function() {
        quantity = this.value;
        document.querySelector('#price').innerHTML = item_price * quantity;
        console.log(`Quantity changed to ${quantity}.`);
    };
    
    // If extra exists,
    if (!(document.getElementById('extra') === null)) {
        // Whenever checkbox checked,
        extra.onchange = function() {
            if (extra.checked) {
                item_price += extra_price;
                document.querySelector('#price').innerHTML = item_price * quantity;
                console.log(`Checked. Price + (${extra_price} * ${quantity})`);
            } else {
                item_price -= extra_price;
                document.querySelector('#price').innerHTML = item_price * quantity;
                console.log(`Unhecked. Price - (${extra_price} * ${quantity})`);
            };
        };
    };
};