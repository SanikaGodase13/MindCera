const token = localStorage.getItem("token");

/* -------------------------
   AUTH CHECK
------------------------- */

if (!token) {
    window.location = "login.html";
}

/* -------------------------
   LOAD DASHBOARD
------------------------- */

async function loadDashboard() {

    try {

        console.log("Dashboard Token:", token);

        const response = await fetch(
            "http://127.0.0.1:8000/dashboard/",
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        console.log("Dashboard Data:", data);

        if (!response.ok) {

            console.error(
                "Dashboard API Error:",
                data
            );

            return;
        }

        /* -------------------------
           USER INFO
        ------------------------- */

        if (
            data.user &&
            document.getElementById("userName")
        ) {

            document.getElementById(
                "userName"
            ).innerText =
                data.user.name || "User";
        }

        /* -------------------------
           OVERVIEW STATS
        ------------------------- */

        if (
            document.getElementById(
                "totalConversations"
            )
        ) {

            document.getElementById(
                "totalConversations"
            ).innerText =
                data.overview?.total_conversations || 0;
        }

        if (
            document.getElementById(
                "totalMessages"
            )
        ) {

            document.getElementById(
                "totalMessages"
            ).innerText =
                data.overview?.total_messages || 0;
        }

        if (
            document.getElementById(
                "totalLogs"
            )
        ) {

            document.getElementById(
                "totalLogs"
            ).innerText =
                data.overview?.total_emotion_logs || 0;
        }

        if (
            document.getElementById(
                "totalAlerts"
            )
        ) {

            document.getElementById(
                "totalAlerts"
            ).innerText =
                data.overview?.total_alerts || 0;
        }

        /* -------------------------
           WELLNESS SECTION
        ------------------------- */

        if (
            document.getElementById(
                "wellnessScore"
            )
        ) {

            document.getElementById(
                "wellnessScore"
            ).innerText =
                (data.wellness?.wellness_score || 0)
                + "%";
        }

        if (
            document.getElementById(
                "dominantEmotion"
            )
        ) {

            document.getElementById(
                "dominantEmotion"
            ).innerText =
                data.wellness?.dominant_emotion
                || "Balanced";
        }

        /* -------------------------
           AI INSIGHT MESSAGE
        ------------------------- */

        const score =
            data.wellness?.wellness_score || 0;

        let insight =
            "Let's continue building healthy emotional habits.";

        if (score >= 80) {

            insight =
                "You're doing great. Keep maintaining your positive wellbeing.";

        } else if (score >= 60) {

            insight =
                "Your emotional wellbeing is stable. Continue self-care practices.";

        } else if (score >= 40) {

            insight =
                "You may be experiencing some emotional challenges. Consider mindfulness or journaling.";

        } else {

            insight =
                "You may need extra support right now. Consider talking to a trusted person or mental health professional.";
        }

        if (
            document.getElementById(
                "aiInsight"
            )
        ) {

            document.getElementById(
                "aiInsight"
            ).innerText =
                insight;
        }

        /* -------------------------
           CHARTS
        ------------------------- */

        if (
            typeof renderEmotionChart === "function" &&
            data.wellness?.emotion_distribution
        ) {

            renderEmotionChart(
                data.wellness.emotion_distribution
            );
        }

        if (
            typeof renderRiskChart === "function" &&
            data.wellness?.risk_distribution
        ) {

            renderRiskChart(
                data.wellness.risk_distribution
            );
        }

    }

    catch (error) {

        console.error(
            "Dashboard Load Error:",
            error
        );
    }
}

/* -------------------------
   PAGE LOAD
------------------------- */

window.addEventListener(
    "DOMContentLoaded",
    loadDashboard
);