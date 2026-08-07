/* =====================================================
   SRI KRISHNA SWACCH AAHARAM ERP

   CUSTOMER INTELLIGENCE ANALYTICS ENGINE

   Stage 15.2.1.3

   Features:
   - RFM Segmentation Chart
   - Customer Spending Chart
   - Customer Value Distribution
   - Premium Animations

===================================================== */



document.addEventListener(
"DOMContentLoaded",
function(){





/* =====================================================
   PAGE VALIDATION
===================================================== */


const customerPage =
document.querySelector(
".customer-page"
);



if(!customerPage){

    return;

}






/* =====================================================
   GET CUSTOMER DATA
===================================================== */


const data =
window.customerAnalytics || {};




const segmentLabels =
data.segmentLabels || [];



const segmentValues =
data.segmentValues || [];




const spendingLabels =
data.spendingLabels || [];



const spendingValues =
data.spendingValues || [];




const valueLabels =
data.valueLabels || [];



const valueValues =
data.valueValues || [];







/* =====================================================
   CHART DEFAULT STYLE
===================================================== */


if(typeof Chart !== "undefined"){


Chart.defaults.font.family =
"Poppins, Arial";


Chart.defaults.plugins.legend.position =
"bottom";


}









/* =====================================================
   CHART CREATOR FUNCTION
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

    return;

}



new Chart(

canvas,

config

);



}









/* =====================================================
   CUSTOMER SEGMENTATION CHART
===================================================== */


createChart(

"segmentChart",

{


type:"doughnut",



data:{


labels:
segmentLabels,


datasets:[{


data:
segmentValues,


borderWidth:2


}]


},




options:{


responsive:true,


maintainAspectRatio:false,


cutout:"65%",



animation:{


duration:1600,


animateRotate:true


},



plugins:{


legend:{


position:"bottom"


}



}



}


}



);











/* =====================================================
   TOP CUSTOMER SPENDING CHART
===================================================== */


createChart(

"spendingChart",

{


type:"bar",



data:{


labels:
spendingLabels,



datasets:[{


label:
"Customer Spending ₹",



data:
spendingValues,



borderWidth:1


}]


},




options:{


responsive:true,


maintainAspectRatio:false,



indexAxis:"y",




animation:{


duration:1500,


easing:"easeOutQuart"


},




scales:{


x:{


beginAtZero:true


}



},



plugins:{


legend:{


position:"bottom"


}



}



}


}



);









/* =====================================================
   CUSTOMER VALUE DISTRIBUTION
===================================================== */


createChart(

"valueChart",

{


type:"bar",




data:{



labels:
valueLabels,



datasets:[{


label:
"Customers",



data:
valueValues,


borderWidth:2


}]



},





options:{


responsive:true,


maintainAspectRatio:false,



animation:{


duration:1500,


easing:"easeOutQuart"


},



scales:{


y:{


beginAtZero:true


}



},



plugins:{


legend:{


position:"bottom"


}



}



}



}



);












/* =====================================================
   KPI CARD ANIMATION
===================================================== */


const cards =
document.querySelectorAll(
".customer-card"
);




cards.forEach(

(card,index)=>{


card.style.opacity="0";


card.style.transform=
"translateY(20px)";




setTimeout(()=>{


card.style.transition=
"all .6s ease";



card.style.opacity="1";


card.style.transform=
"translateY(0)";



},

index*120);



}

);









/* =====================================================
   SEGMENT CARD ANIMATION
===================================================== */


const segmentCards =
document.querySelectorAll(
".segment-card"
);




segmentCards.forEach(

(card,index)=>{


card.style.opacity="0";



setTimeout(()=>{


card.style.transition=
"all .5s ease";


card.style.opacity="1";


},

index*150);



}

);









/* =====================================================
   SCORE CIRCLE ANIMATION
===================================================== */


const score =
document.querySelector(
".score-circle"
);



if(score){


score.style.transform=
"scale(.8)";


score.style.opacity="0";



setTimeout(()=>{


score.style.transition=
"all .8s ease";


score.style.transform=
"scale(1)";


score.style.opacity="1";



},300);



}






});