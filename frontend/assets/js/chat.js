const token =
localStorage.getItem("token");

if(!token){

    window.location =
    "login.html";
}

let currentConversationId = null;

// SEND MESSAGE
async function sendMessage() {

    const input = document.getElementById("messageInput");
    const message = input.value;

    if (!message) return;

    appendMessage("user", message);

    input.value = "";

    const token = localStorage.getItem("token");

const res = await fetch(
    "http://127.0.0.1:8000/chat/send",
{
    method: "POST",

    headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    },

    body: JSON.stringify({
        conversation_id: currentConversationId,
        message: message
    })
});

    const data = await res.json();

    appendMessage("ai", data.ai_response);
    speakAI(data.ai_response);

    // OPTIONAL: show recommendations (future upgrade)
    console.log(data.recommendations);
}

// UI RENDER FUNCTION
function appendMessage(
role,
text
){

const chatBox =
document.getElementById(
"chatBox"
);

const wrapper =
document.createElement("div");

wrapper.className =
`message ${role}`;

const avatar =
role === "user"
?
"👤"
:
"🧠";

wrapper.innerHTML = `

<div class="avatar">

${avatar}

</div>

<div class="bubble">

${text}

</div>

`;

chatBox.appendChild(wrapper);

chatBox.scrollTop =
chatBox.scrollHeight;
}


function scrollToBottom() {
    const chatBox = document.getElementById("chatBox");
    chatBox.scrollTop = chatBox.scrollHeight;
}

document.getElementById("messageInput")
.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

async function loadConversations() {

    const token =
        localStorage.getItem("token");

    const response = await fetch(
        "http://127.0.0.1:8000/chat/conversations",
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    const data =
await response.json();

const conversations =
data.conversations;



    const container =
        document.getElementById(
            "conversationList"
        );

    container.innerHTML = "";

    conversations.forEach(conv => {

        container.innerHTML += `

            <div
                class="conversation-item"

                onclick="loadMessages(${conv.id})"
            >

                Wellness Chat #${conv.id}

            </div>

        `;
    });
}

async function createConversation() {

    const token =
        localStorage.getItem("token");

    const response = await fetch(
        "http://127.0.0.1:8000/chat/conversation",
        {
            method:"POST",

            headers:{
                Authorization:`Bearer ${token}`
            }
        }
    );

    const data =
        await response.json();

    currentConversationId =
        data.conversation_id;

    document.getElementById(
        "chatBox"
    ).innerHTML = "";

    loadConversations();
}

async function loadMessages(
    conversationId
) {

    currentConversationId =
        conversationId;

    const token =
        localStorage.getItem("token");

    const response = await fetch(

        `http://127.0.0.1:8000/chat/history/${conversationId}`,

        {
            headers:{
                Authorization:`Bearer ${token}`
            }
        }
    );

    const responseData =
    await response.json();

const messages =
    responseData.messages || [];

const chatBox =
    document.getElementById("chatBox");

chatBox.innerHTML = "";

   messages.forEach(msg => {

    appendMessage(
        msg.role === "assistant"
            ? "ai"
            : "user",
        msg.message
    );

});
    scrollToBottom();
}

window.onload = async () => {

    await loadConversations();

    if(currentConversationId === null){

        await createConversation();
    }
};


function quickPrompt(text){

document.getElementById(
"messageInput"
).value = text;

sendMessage();
}
