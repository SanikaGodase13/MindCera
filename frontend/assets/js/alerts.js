const token = localStorage.getItem("token");

if (!token) {
    window.location = "login.html";
}

// -----------------------------
// LOAD ALERTS
// -----------------------------
async function loadAlerts() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/alerts/",
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {
            throw new Error("Failed to load alerts");
        }

        const alerts = await response.json();

        // -----------------------------
        // SUMMARY CARDS
        // -----------------------------
        document.getElementById("totalAlerts").innerText =
            alerts.length;

        document.getElementById("activeAlerts").innerText =
            alerts.filter(
                a => a.status === "ACTIVE"
            ).length;

        document.getElementById("highRiskAlerts").innerText =
            alerts.filter(
                a => a.risk_level === "HIGH"
            ).length;

        const container =
            document.getElementById(
                "alertsContainer"
            );

        container.innerHTML = "";

        // -----------------------------
        // NO ALERTS UI
        // -----------------------------
        if (alerts.length === 0) {

            container.innerHTML = `

                <div class="alert-card">

                    <h3>
                        🎉 No Alerts Detected
                    </h3>

                    <div class="alert-message">

                        MindCera has not detected any
                        emotional risk events.

                        Continue your wellness journey
                        and maintain healthy habits.

                    </div>

                </div>

            `;

            return;
        }

        // -----------------------------
        // ALERT CARDS
        // -----------------------------
        alerts.forEach(alert => {

            let riskClass = "alert-low";

            if (alert.risk_level === "HIGH") {

                riskClass = "alert-high";

            } else if (
                alert.risk_level === "MEDIUM"
            ) {

                riskClass = "alert-medium";
            }

            container.innerHTML += `

                <div class="alert-card ${riskClass}">

                    <div class="alert-top">

                        <h3>

                            Emotional Wellness Alert

                        </h3>

                        <div class="alert-badge">

                            ${alert.risk_level}

                        </div>

                    </div>

                    <div class="alert-message">

                        ${alert.message}

                    </div>

                    <div class="alert-date">

                        ${new Date(
                            alert.created_at
                        ).toLocaleString()}

                    </div>

                </div>

            `;
        });

    } catch (error) {

        console.error(
            "Alert loading error:",
            error
        );

        document.getElementById(
            "alertsContainer"
        ).innerHTML = `

            <div class="alert-card">

                <h3>
                    ⚠ Unable to Load Alerts
                </h3>

                <div class="alert-message">

                    Something went wrong while
                    loading alerts.

                    Please try again later.

                </div>

            </div>

        `;
    }
}

// -----------------------------
// INITIAL LOAD
// -----------------------------
loadAlerts();