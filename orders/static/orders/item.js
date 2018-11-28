document.addEventListener('DOMContentLoaded', () => {
    item_price = document.querySelector('#price').innerHTML;

    document.querySelector('#quantity').onchange = function() {
        quantity = this.value;
        document.querySelector('#price').innerHTML = item_price * quantity;
    };

    extra_cheese_price = document.querySelector('#extra_cheese_price').innerHTML;
    extra_cheese.onchange = function() {
        if (extra_cheese.checked) {
            document.querySelector('#price').innerHTML = parseInt(document.querySelector('#price').innerHTML) + (parseInt(quantity) * parseInt(extra_cheese_price));
        } else {
            document.querySelector('#price').innerHTML = parseInt(document.querySelector('#price').innerHTML) - (parseInt(quantity) * parseInt(extra_cheese_price));
        }
    };
});