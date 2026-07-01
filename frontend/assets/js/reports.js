const token =
localStorage.getItem("token");

if(!token){

    window.location =
    "login.html";
}

loadCharts();

function loadCharts(){

    // Wellness Trend

    new Chart(

        document.getElementById(
            "emotionTrendChart"
        ),

        {

            type:"line",

            data:{

                labels:[
                    "Mon",
                    "Tue",
                    "Wed",
                    "Thu",
                    "Fri",
                    "Sat",
                    "Sun"
                ],

                datasets:[{

                    label:"Wellness Score",

                    data:[
                        65,
                        72,
                        70,
                        75,
                        80,
                        85,
                        78
                    ],

                    tension:.4,

                    fill:true,

                    backgroundColor:
                    "rgba(99,102,241,.15)",

                    borderColor:
                    "#6366F1",

                    borderWidth:3
                }]
            },

            options:{
                responsive:true
            }
        }
    );

    // Risk Distribution

    new Chart(

        document.getElementById(
            "riskTrendChart"
        ),

        {

            type:"doughnut",

            data:{

                labels:[
                    "Low",
                    "Medium",
                    "High"
                ],

                datasets:[{

                    data:[
                        12,
                        3,
                        1
                    ],

                    backgroundColor:[

                        "#22C55E",
                        "#F59E0B",
                        "#EF4444"
                    ]
                }]
            }
        }
    );
}

function downloadReport(){

    window.print();
}