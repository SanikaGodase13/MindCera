let emotionChartInstance = null;
let riskChartInstance = null;

/* ==========================
   EMOTION CHART
========================== */

function renderEmotionChart(emotions) {

    const canvas =
        document.getElementById(
            "emotionChart"
        );

    if (!canvas) return;

    if (emotionChartInstance) {
        emotionChartInstance.destroy();
    }

    emotionChartInstance =
        new Chart(canvas, {

            type: "doughnut",

            data: {

                labels:
                    Object.keys(emotions),

                datasets: [{

                    data:
                        Object.values(emotions),

                    backgroundColor: [

                        "#7C83FD",
                        "#A5D8FF",
                        "#CDB4DB",
                        "#FFC8DD",
                        "#B8F2E6",
                        "#FFD6A5",
                        "#FEC5BB"

                    ],

                    borderWidth: 0

                }]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        position: "bottom"

                    }

                }

            }

        });
}

/* ==========================
   RISK CHART
========================== */

function renderRiskChart(risks) {

    const canvas =
        document.getElementById(
            "riskChart"
        );

    if (!canvas) return;

    if (riskChartInstance) {
        riskChartInstance.destroy();
    }

    riskChartInstance =
        new Chart(canvas, {

            type: "bar",

            data: {

                labels:
                    Object.keys(risks),

                datasets: [{

                    label:
                        "Risk Level",

                    data:
                        Object.values(risks),

                    backgroundColor: [

                        "#22C55E",
                        "#F59E0B",
                        "#EF4444"

                    ],

                    borderRadius: 12

                }]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        display: false

                    }

                },

                scales: {

                    y: {

                        beginAtZero: true,

                        ticks: {

                            precision: 0

                        }

                    }

                }

            }

        });
}