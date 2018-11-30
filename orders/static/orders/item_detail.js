document.addEventListener('DOMContentLoaded', () => {
    // Subtotal
    item_price = document.querySelector('#price').innerHTML;

    quantity = 1;
    document.querySelector('#quantity').onchange = function() {
        quantity = this.value;
        document.querySelector('#price').innerHTML = item_price * quantity;
    };

    extra.onchange = function() {
        extra_price = document.querySelector('#extra_price').innerHTML;
        price = parseInt(document.querySelector('#price').innerHTML);
        extra_price = parseInt(quantity) * parseInt(extra_price);
        if (extra.checked) {
            document.querySelector('#price').innerHTML = price + extra_price;
        } else {
            document.querySelector('#price').innerHTML = price - extra_price;
        }
    };
});