/* =====================================================
   SRI KRISHNA SWACCH AAHARAM
   PREMIUM BUSINESS INTELLIGENCE DASHBOARD JS

   SAFE STAGE 12.4 FIX
   Chart + KPI + BI Animations

===================================================== */


document.addEventListener(
"DOMContentLoaded",
function(){


/* =====================================================
   CHECK CHART.JS
===================================================== */


if(typeof Chart === "undefined"){

    console.error(
        "Chart.js not loaded"
    );

    return;

}





/* =====================================================
   KPI COUNTER ANIMATION
===================================================== */


const counters =
document.querySelectorAll(
".counter"
);



counters.forEach(counter => {

    const target = Number(counter.dataset.value || 0);

    const isCurrency =
        counter.dataset.currency === "true";

    let current = 0;

    const increment =
        target / 60;

    function animate() {

        current += increment;

        if (current < target) {

            const value = Math.floor(current);

            counter.innerHTML = isCurrency
                ? "₹" + value.toLocaleString("en-IN")
                : value.toLocaleString("en-IN");

            requestAnimationFrame(animate);

        } else {

            counter.innerHTML = isCurrency
                ? "₹" + target.toLocaleString("en-IN")
                : target.toLocaleString("en-IN");

        }

    }

    animate();

});






/* =====================================================
   GET DASHBOARD DATA
   FIXED CONNECTION WITH dashboard.html
===================================================== */


const dashboardData =
window.dashboardData || {};




const salesLabels =
dashboardData.salesLabels || [];

const salesValues =
dashboardData.salesValues || [];



const categoryLabels =
dashboardData.categoryLabels || [];

const categoryValues =
dashboardData.categoryValues || [];



const inventoryLabels =
dashboardData.inventoryLabels || [];

const inventoryValues =
dashboardData.inventoryValues || [];



const topProductNames =
dashboardData.topProductNames || [];

const topProductSales =
dashboardData.topProductSales || [];









/* =====================================================
   CHART DEFAULT SETTINGS
===================================================== */


Chart.defaults.font.family =
"Poppins, Arial";



Chart.defaults.plugins.legend.position =
"bottom";



Chart.defaults.plugins.legend.labels.padding =
20;








/* =====================================================
   SAFE CHART CREATOR
===================================================== */


function createChart(
canvasId,
config
){


const canvas =
document.getElementById(
canvasId
);



if(!canvas){

    console.warn(
        canvasId + " not found"
    );

    return;

}



if(canvas.chart){

    canvas.chart.destroy();

}



canvas.chart =
new Chart(
canvas,
config
);



}








/* =====================================================
   REVENUE TREND
===================================================== */


createChart(

"salesChart",

{


type:"line",


data:{


labels:salesLabels,


datasets:[{


label:"Revenue ₹",


data:salesValues,


borderWidth:3,


tension:.4,


fill:true


}]


},



options:{


responsive:true,


maintainAspectRatio:false,


animation:{


duration:1500


}


}


}

);









/* =====================================================
   CATEGORY SALES
===================================================== */


createChart(

"categoryChart",

{


type:"doughnut",



data:{


labels:categoryLabels,


datasets:[{


data:categoryValues,


borderWidth:2


}]


},



options:{


responsive:true,


maintainAspectRatio:false,


cutout:"65%"


}


}


);









/* =====================================================
   INVENTORY HEALTH
===================================================== */


createChart(

"inventoryChart",

{


type:"doughnut",



data:{


labels:inventoryLabels,


datasets:[{


data:inventoryValues,


borderWidth:2


}]


},



options:{


responsive:true,


maintainAspectRatio:false,


cutout:"60%"


}



}



);









/* =====================================================
   TOP PRODUCTS
===================================================== */


createChart(

"topProductsChart",

{


type:"bar",



data:{


labels:topProductNames,


datasets:[{


label:"Revenue Generated ₹",


data:topProductSales,


borderWidth:1


}]


},



options:{


responsive:true,


maintainAspectRatio:false,


indexAxis:"y",



scales:{


x:{


beginAtZero:true


}


}



}



}



);












/* =====================================================
   PREMIUM CARD HOVER
===================================================== */


const cards =
document.querySelectorAll(
".premium-card"
);



cards.forEach(card=>{


card.addEventListener(
"mouseenter",
()=>{


card.style.transform =
"translateY(-6px)";


}
);



card.addEventListener(
"mouseleave",
()=>{


card.style.transform =
"translateY(0)";


}


);



});







});










/* =====================================================
   ADVANCED BI ANIMATIONS
===================================================== */


document.addEventListener(
"DOMContentLoaded",
function(){





/* BI NUMBER COUNTERS */


const biNumbers =
document.querySelectorAll(
".bi-card h2"
);



biNumbers.forEach(element=>{


let original =
element.innerText;



let number =
parseFloat(
original.replace(
/[^0-9.]/g,
""
)
);



if(isNaN(number))
return;



let current = 0;


let step =
number / 50;



function run(){


current += step;



if(current < number){


if(original.includes("%")){


element.innerHTML =
Math.floor(current)+"%";


}

else if(
original.includes("₹")
){


element.innerHTML =
"₹"+
Math.floor(current)
.toLocaleString();


}

else{


element.innerHTML =
Math.floor(current)
.toLocaleString();


}



requestAnimationFrame(run);


}

else{


element.innerHTML =
original;


}



}



run();



});








/* BUSINESS HEALTH EFFECT */


const health =
document.querySelector(
".bi-card:last-child h2"
);



if(health){


health.style.transition =
"0.8s";


health.style.transform =
"scale(1.05)";


setTimeout(()=>{


health.style.transform =
"scale(1)";


},800);



}







/* REVENUE GROWTH INDICATOR */


const growth =
document.querySelector(
".growth-value"
);



if(growth){


let value =
parseFloat(
growth.innerText
);



if(value>0){


growth.innerHTML =
"⬆ "+growth.innerHTML;


}



else if(value<0){


growth.innerHTML =
"⬇ "+growth.innerHTML;


}



}





/* DASHBOARD ENTRY ANIMATION */


const dashboard =
document.querySelector(
".dashboard-container"
);



if(dashboard){


dashboard.style.opacity="0";


setTimeout(()=>{


dashboard.style.transition=
"0.6s";


dashboard.style.opacity="1";


},100);



}



});