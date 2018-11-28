document.addEventListener('DOMContentLoaded', () => {
    item_price = document.querySelector('#price').innerHTML;

    quantity = 1;
    document.querySelector('#quantity').onchange = function() {
        quantity = this.value;
        document.querySelector('#price').innerHTML = item_price * quantity;
    };

    extra_cheese.onchange = function() {
        extra_cheese_price = document.querySelector('#extra_cheese_price').innerHTML;
        price = parseInt(document.querySelector('#price').innerHTML);
        extra_price = parseInt(quantity) * parseInt(extra_cheese_price);
        if (extra_cheese.checked) {
            document.querySelector('#price').innerHTML = price + extra_price;
        } else {
            document.querySelector('#price').innerHTML = price - extra_price;
        }
    };
});