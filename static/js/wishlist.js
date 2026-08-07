document.addEventListener(
"DOMContentLoaded",
function(){



/* =====================================================
   ADD PRODUCT TO WISHLIST
===================================================== */


document.querySelectorAll(
".wishlist-btn"
)
.forEach(button=>{


button.addEventListener(
"click",
function(){


let productId =
this.dataset.id;



fetch(
"/add-wishlist/"+productId,
{

method:"POST"

}

)


.then(
response=>response.json()
)


.then(
data=>{


if(data.success){


this.innerHTML="♥";


this.classList.add(
"active"
);



showWishlistToast(
"❤️ Product added to wishlist"
);



updateWishlistBadge(
data.wishlist_count
);



}


else{


showWishlistToast(
"⚠️ Already in wishlist"
);



}



})


.catch(
error=>{


console.log(
"Wishlist Error:",
error
);


showWishlistToast(
"Unable to add wishlist"
);


});


});


});








/* =====================================================
   REMOVE PRODUCT FROM WISHLIST
===================================================== */


document.querySelectorAll(
".remove-wishlist-btn"
)
.forEach(button=>{


button.addEventListener(
"click",
function(){



let wishlistId =
this.dataset.id;



let card =
this.closest(
".wishlist-card"
);




fetch(
"/remove-wishlist/"+wishlistId
)



.then(
response=>response.json()
)



.then(
data=>{


if(data.success){



if(card){

card.remove();

}



showWishlistToast(
"🗑 Product removed from wishlist"
);



updateWishlistBadge(
data.wishlist_count
);



}



else{


showWishlistToast(
"⚠️ Unable to remove product"
);


}



})



.catch(
error=>{


console.log(
"Remove Wishlist Error:",
error
);


showWishlistToast(
"Something went wrong"
);


});



});


});







/* =====================================================
   CLEAR COMPLETE WISHLIST
===================================================== */


const clearButton =
document.querySelector(
".clear-wishlist-btn"
);



if(clearButton){



clearButton.addEventListener(
"click",
function(event){



event.preventDefault();



let confirmDelete =
confirm(
"Are you sure you want to clear wishlist?"
);



if(!confirmDelete){

return;

}




fetch(
this.href
)



.then(
response=>response.json()
)



.then(
data=>{


if(data.success){



document.querySelectorAll(
".wishlist-card"
)
.forEach(
card=>{

card.remove();

}

);



showWishlistToast(
"🗑 Wishlist cleared successfully"
);



updateWishlistBadge(
0
);



}



});



});



}



});









/* =====================================================
   UPDATE WISHLIST BADGE
===================================================== */


function updateWishlistBadge(
count
){



let badge =
document.querySelector(
".wishlist-count"
);



if(badge){


badge.innerText =
count;


}



}









/* =====================================================
   COMMON TOP RIGHT NOTIFICATION
===================================================== */


function showWishlistToast(message){

    let notification =
    document.getElementById(
        "notification"
    );


    if(!notification){

        return;

    }


    notification.innerHTML =
    message;


    notification.classList.add(
        "show"
    );


    setTimeout(
        ()=>{

            notification.classList.remove(
                "show"
            );

        },
        2500
    );

}