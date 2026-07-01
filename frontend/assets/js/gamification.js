const token =
localStorage.getItem("token");

if(!token){

    window.location =
    "login.html";
}

console.log(
    "MindCera Wellness Journey Loaded"
);

// Future API Integration

async function loadGamificationData(){

    try{

        // Future endpoint:
        // GET /gamification

        console.log(
            "Gamification Ready"
        );

    }
    catch(error){

        console.log(error);
    }
}

loadGamificationData();