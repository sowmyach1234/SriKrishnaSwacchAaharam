const minus = document.getElementById("minusBtn");
const plus = document.getElementById("plusBtn");
const quantity = document.getElementById("quantity");

if (minus && plus && quantity) {

    minus.onclick = function () {

        let value = parseInt(quantity.value);

        if (value > 1) {

            quantity.value = value - 1;

        }

    };

    plus.onclick = function () {

        let value = parseInt(quantity.value);

        quantity.value = value + 1;

    };

}