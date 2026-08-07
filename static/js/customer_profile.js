document.addEventListener(
"DOMContentLoaded",
function(){



const trend =
document.getElementById(
"purchaseTrendChart"
);



if(trend){


new Chart(
trend,
{


type:"line",


data:{


labels:
window.customerMonthlyLabels,


datasets:[

{


label:
"Purchase Amount",


data:
window.customerMonthlyValues,


borderWidth:3,


tension:.4

}


]


},



options:{


responsive:true,


plugins:{


legend:{


display:true


}


}



}


}

);


}









const category =
document.getElementById(
"categoryPreferenceChart"
);


if(category && 
window.customerCategoryLabels.length > 0){


new Chart(
category,
{

type:"doughnut",


data:{


labels:
window.customerCategoryLabels,


datasets:[

{

data:
window.customerCategoryValues,


backgroundColor:[

"#2f6b3f",
"#7cb342",
"#d4a017",
"#8d6e63"

],


borderWidth:2


}

]


},



options:{


responsive:true,


plugins:{


legend:{


position:"bottom"


}


}


}


}

);


}
else{

console.log(
"No category data available",
window.customerCategoryLabels,
window.customerCategoryValues
);


}



});