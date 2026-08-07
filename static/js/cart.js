document.addEventListener(
"DOMContentLoaded",
function(){



/* =====================================================
   ADD TO CART FROM WEBSITE
   Home / Products / Product Details
===================================================== */


document.querySelectorAll(
".add-cart-btn, .add-detail-cart"
)
.forEach(button=>{


button.addEventListener(
"click",
function(){


let productId =
this.dataset.id;


let quantity = 1;



const quantityInput =
document.getElementById(
"selected-quantity"
);



if(quantityInput){

quantity =
parseInt(
quantityInput.value
);

}



addToCart(
productId,
quantity
);



});


});


/* =====================================================
   HOME + PRODUCT PAGE ADD TO CART
===================================================== */


document.querySelectorAll(
".add-cart-btn"
)
.forEach(button=>{


button.addEventListener(
"click",
function(){


let productId =
this.dataset.id;



addToCart(
productId,
1
);



});



});





/* =====================================================
   PRODUCT DETAIL QUANTITY
===================================================== */


let quantity = 1;


const quantityDisplay =
document.getElementById(
"quantity"
);



const quantityInput =
document.getElementById(
"selected-quantity"
);



const plus =
document.getElementById(
"plus"
);



const minus =
document.getElementById(
"minus"
);





if(plus){


plus.onclick=function(){


quantity++;


if(quantityDisplay)
quantityDisplay.innerText=quantity;


if(quantityInput)
quantityInput.value=quantity;



};


}




if(minus){


minus.onclick=function(){


if(quantity>1){

quantity--;

}



if(quantityDisplay)
quantityDisplay.innerText=quantity;



if(quantityInput)
quantityInput.value=quantity;



};



}








/* =====================================================
   CART PAGE PLUS
===================================================== */


document.querySelectorAll(
".cart-plus"
)
.forEach(button=>{


button.onclick=function(){


let cartId =
this.dataset.id;



let qty =
document.getElementById(
"quantity-"+cartId
);



let quantity =
parseInt(
qty.innerText
);



quantity++;



updateCartQuantity(
cartId,
quantity
);



};



});









/* =====================================================
   CART PAGE MINUS
===================================================== */


document.querySelectorAll(
".cart-minus"
)
.forEach(button=>{


button.onclick=function(){


let cartId =
this.dataset.id;



let qty =
document.getElementById(
"quantity-"+cartId
);



let quantity =
parseInt(
qty.innerText
);



if(quantity>1){

quantity--;

updateCartQuantity(
cartId,
quantity
);


}



};



});









/* =====================================================
 REMOVE PRODUCT
===================================================== */


document.querySelectorAll(
".premium-remove-btn"
)
.forEach(button=>{


button.onclick=function(event){


event.preventDefault();



let card =
this.closest(
".premium-cart-card"
);



fetch(
this.href
)


.then(()=>{


card.remove();



showToast(
"🗑 Product removed"
);



updateCartSummary();



});


};



});





});









/* =====================================================
 ADD TO CART API
===================================================== */


function addToCart(
productId,
quantity
){


fetch(
"/add-to-cart/"+productId,
{


method:"POST",


headers:{

"Content-Type":
"application/json"

},


body:JSON.stringify({

quantity:quantity

})


}

)



.then(
response=>response.json()
)



.then(
data=>{


if(data.success){


updateCartBadge(
data.cart_count
);



showToast(
"🌿 Product added to cart"
);



}

else{


showToast(
"⚠️ "+data.message
);



}



});


}









/* =====================================================
 UPDATE CART QUANTITY
===================================================== */


function updateCartQuantity(
cartId,
quantity
){


fetch(
"/update-cart-quantity/"+cartId,
{


method:"POST",


headers:{

"Content-Type":
"application/json"

},


body:JSON.stringify({

quantity:quantity

})


}

)


.then(
response=>response.json()
)


.then(
data=>{


if(data.success){



document.getElementById(
"quantity-"+cartId
).innerText =
quantity;



document.getElementById(
"subtotal-"+cartId
).innerText =
"₹"+data.subtotal;



document.getElementById(
"cart-total-items"
).innerText =
data.total_items;



document.getElementById(
"cart-grand-total"
).innerText =
"₹"+data.grand_total;




showToast(
"🌿 Cart updated"
);



}


});


}









/* =====================================================
 CART SUMMARY
===================================================== */


function updateCartSummary(){


fetch(
"/cart-summary"
)


.then(
response=>response.json()
)


.then(
data=>{


let total =
document.getElementById(
"cart-total-items"
);



if(total){

total.innerText =
data.items;

}



let amount =
document.getElementById(
"cart-grand-total"
);



if(amount){

amount.innerText =
"₹"+data.total;

}



updateCartBadge(
data.items
);



});


}









/* =====================================================
 CART BADGE
===================================================== */


function updateCartBadge(
count
){


document.querySelectorAll(
".cart-count,.cart b"
)
.forEach(
badge=>{

badge.innerText=count;

}

);


}



function showToast(message){

    let notification =
    document.getElementById("notification");


    if(!notification){
        return;
    }


    notification.innerHTML = message;


    notification.classList.add("show");


    setTimeout(()=>{

        notification.classList.remove("show");

    },2500);

}






function addToCart(productId, quantity){


fetch(
"/add-to-cart/"+productId,
{

method:"POST",

headers:{

"Content-Type":
"application/json"

},

body:JSON.stringify({

quantity:quantity

})

}

)



.then(response=>response.json())


.then(data=>{


if(data.success){



updateCartBadge(
data.cart_count
);



showToast(
"🌿 Product added to cart"
);



}

else{


showToast(
"⚠️ "+data.message
);


}



})



.catch(error=>{


console.log(
"Cart Error:",
error
);


showToast(
"Unable to add product"
);


});


}