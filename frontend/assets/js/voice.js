let recognition = null;

let isListening = false;

let voiceEnabled = true;

/* =========================
START VOICE INPUT
========================= */

function startVoice() {


const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

if (!SpeechRecognition) {

    alert(
        "Speech Recognition is not supported in your browser."
    );

    return;
}

if (!recognition) {

    recognition =
        new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.continuous = false;

    recognition.interimResults = false;

    recognition.maxAlternatives = 1;

    /* -------------------------
       VOICE RESULT
    ------------------------- */

    recognition.onresult =
        function(event) {

            const text =
                event.results[0][0].transcript;

            document.getElementById(
                "messageInput"
            ).value = text;

            stopVoice();

            if (
                typeof sendMessage ===
                "function"
            ) {

                sendMessage();
            }
        };

    /* -------------------------
       ERROR HANDLING
    ------------------------- */

    recognition.onerror =
        function(event) {

            console.log(
                "Voice Error:",
                event.error
            );

            stopVoice();
        };

    /* -------------------------
       LISTENING FINISHED
    ------------------------- */

    recognition.onend =
        function() {

            isListening = false;

            const indicator =
                document.getElementById(
                    "voiceIndicator"
                );

            if(indicator){

                indicator.style.display =
                    "none";
            }
        };
}

if(!isListening){

    recognition.start();

    isListening = true;

    const indicator =
        document.getElementById(
            "voiceIndicator"
        );

    if(indicator){

        indicator.style.display =
            "block";
    }
}


}

/* =========================
STOP VOICE
========================= */

function stopVoice() {


if(
    recognition &&
    isListening
){

    recognition.stop();

    isListening = false;
}

const indicator =
    document.getElementById(
        "voiceIndicator"
    );

if(indicator){

    indicator.style.display =
        "none";
}


}

/* =========================
TOGGLE SPEECH
========================= */

function toggleSpeech() {


voiceEnabled =
    !voiceEnabled;

const status =
    voiceEnabled
        ? "Voice Enabled 🔊"
        : "Voice Disabled 🔇";

alert(status);


}

/* =========================
SPEAK AI RESPONSE
========================= */

function speakAI(text) {


if(!voiceEnabled){

    return;
}

window.speechSynthesis.cancel();

const speech =
    new SpeechSynthesisUtterance(
        text
    );

speech.rate = 0.95;

speech.pitch = 1;

speech.volume = 1;

speech.lang = "en-US";

const voices =
    window.speechSynthesis.getVoices();

const preferredVoice =
    voices.find(v =>
        v.name.includes("Google")
    ) ||
    voices.find(v =>
        v.lang.includes("en")
    );

if(preferredVoice){

    speech.voice =
        preferredVoice;
}

window.speechSynthesis.speak(
    speech
);


}

/* =========================
STOP AI SPEAKING
========================= */

function stopSpeaking() {


window.speechSynthesis.cancel();


}

/* =========================
INIT VOICE SYSTEM
========================= */

function initVoice() {


if(
    "speechSynthesis" in window
){

    window.speechSynthesis.getVoices();
}


}
