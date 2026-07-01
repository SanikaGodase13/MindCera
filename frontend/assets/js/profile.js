const token =
localStorage.getItem("token");

if(!token){

    window.location =
    "login.html";
}

async function loadProfile(){

    try{

        const response =
        await fetch(

            "http://127.0.0.1:8000/auth/profile",

            {
                headers:{
                    Authorization:
                    `Bearer ${token}`
                }
            }
        );

        const user =
        await response.json();

        document.getElementById(
            "userName"
        ).innerText =
        user.name;

        document.getElementById(
            "userEmail"
        ).innerText =
        user.email;

        document.getElementById(
            "userAge"
        ).innerText =
        user.age || "-";

        document.getElementById(
            "userGender"
        ).innerText =
        user.gender || "-";

        document.getElementById(
            "userOccupation"
        ).innerText =
        user.occupation || "-";

        document.getElementById(
            "userGoal"
        ).innerText =
        user.mental_health_goal || "-";

        document.getElementById(
            "guardianName"
        ).innerText =
        user.guardian_name || "-";

        document.getElementById(
            "guardianEmail"
        ).innerText =
        user.guardian_email || "-";

        document.getElementById(
            "guardianPhone"
        ).innerText =
        user.guardian_phone || "-";

        document.getElementById(
            "profileAvatar"
        ).src =
        `https://ui-avatars.com/api/?name=${encodeURIComponent(user.name)}&background=6366F1&color=fff`;

    }
    catch(error){

        console.error(error);
    }
}

function logout(){

    localStorage.removeItem(
        "token"
    );

    window.location =
    "login.html";
}

loadProfile();