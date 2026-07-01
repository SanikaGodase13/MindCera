const token = localStorage.getItem("token");

if(!token){
    window.location = "login.html";
}

let timerInterval;
let audio;

// ----------------------
// BREATHING SESSION
// ----------------------

function startBreathing(){

    const circle =
    document.getElementById(
        "breathingCircle"
    );

    const status =
    document.getElementById(
        "breathingStatus"
    );

    status.innerText =
    "Inhale...";

    circle.style.transform =
    "scale(1.5)";

    setTimeout(()=>{

        status.innerText =
        "Exhale...";

        circle.style.transform =
        "scale(1)";

    },4000);

    setTimeout(()=>{

        status.innerText =
        "Complete ✔";

    },8000);
}

// ----------------------
// TIMER
// ----------------------

function startTimer(minutes){

    clearInterval(timerInterval);

    let seconds =
    minutes * 60;

    updateTimer(seconds);

    timerInterval =
    setInterval(()=>{

        seconds--;

        updateTimer(seconds);

        if(seconds <= 0){

            clearInterval(
                timerInterval
            );

            alert(
                "Meditation Session Complete 🧘"
            );
        }

    },1000);
}

function updateTimer(seconds){

    const min =
    Math.floor(seconds/60);

    const sec =
    seconds%60;

    document.getElementById(
        "timerDisplay"
    ).innerText =

    `${String(min).padStart(2,'0')}:${String(sec).padStart(2,'0')}`;
}

// ----------------------
// SOUNDS
// ----------------------

function playSound(type){

    stopSound();

    const files = {

        rain:
        "assets/audio/rain.mp3",

        ocean:
        "assets/audio/ocean.mp3",

        forest:
        "assets/audio/forest.mp3"
    };

    audio =
    new Audio(files[type]);

    audio.loop = true;

    audio.play();
}

function stopSound(){

    if(audio){

        audio.pause();

        audio.currentTime = 0;
    }
}

// ----------------------
// DAILY QUOTES
// ----------------------

const quotes = [

"Every breath is a new beginning.",

"Healing takes time. Give yourself grace.",

"Peace begins when expectations end.",

"You are stronger than your thoughts.",

"Small steps every day create big changes.",

"The present moment is enough."
];

document.getElementById(
    "quote"
).innerText =

quotes[
    Math.floor(
        Math.random() *
        quotes.length
    )
];