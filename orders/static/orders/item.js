document.addEventListener('DOMContentLoaded', () => {
    price = document.querySelector('#price').innerHTML;
    document.querySelector('#quantity').onchange = function() {
        document.querySelector('#price').innerHTML = this.value * price;
    }
});