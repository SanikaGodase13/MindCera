async function register() {

    const data = {

    name:
    document.getElementById("name").value,

    email:
    document.getElementById("email").value,

    password:
    document.getElementById("password").value,

    age:
    parseInt(
        document.getElementById("age").value
    ),

    gender:
    document.getElementById("gender").value,

    occupation:
    document.getElementById("occupation").value,

    mental_health_goal:
    document.getElementById("goal").value,

    guardian_name:
    document.getElementById("guardianName").value,

    guardian_email:
    document.getElementById("guardianEmail").value,

    guardian_phone:
    document.getElementById("guardianPhone").value


};


    const response =
    await fetch(

        `${API_BASE}/auth/register`,

        {

            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:
            JSON.stringify(data)
        }
    );

    if(response.ok){

        const button =
            document.querySelector(".register-btn");

            button.innerHTML =
                "✅ Registration Successful";

            setTimeout(() => {

                window.location =
                    "login.html";

            }, 1500);
    }
}

async function login(){

    const formData =
    new URLSearchParams();

    formData.append(
        "username",
        document.getElementById("email").value
    );

    formData.append(
        "password",
        document.getElementById("password").value
    );

    const response =
    await fetch(

        `${API_BASE}/auth/login`,

        {

            method:"POST",

            headers:{
                "Content-Type":
                "application/x-www-form-urlencoded"
            },

            body:formData
        }
    );

    const data =
    await response.json();

    localStorage.setItem(
        "token",
        data.access_token
    );

    const button =
        document.querySelector(".register-btn");

    button.innerHTML =
        "✅ Login Successful";

    setTimeout(() => {

        window.location =
            "dashboard.html";

    }, 1200);
}

function togglePassword() {


const password =
document.getElementById("password");

if(password.type === "password") {

    password.type = "text";

} else {

    password.type = "password";
}


}

async function sendOTP() {


const response =
await fetch(
    `${API_BASE}/auth/forgot-password`,
    {
        method:"POST",

        headers:{
            "Content-Type":
            "application/json"
        },

        body:JSON.stringify({
            email:
            document.getElementById("email").value
        })
    }
);

if(response.ok){

    alert("OTP Sent");

    window.location =
    "verify-otp.html";
}


}

async function verifyOTP() {


const response =
await fetch(
    `${API_BASE}/auth/verify-otp`,
    {
        method:"POST",

        headers:{
            "Content-Type":
            "application/json"
        },

        body:JSON.stringify({

            email:
            document.getElementById("email").value,

            otp:
            document.getElementById("otp").value
        })
    }
);

if(response.ok){

    alert("OTP Verified");

    window.location =
    "reset-password.html";
}


}

async function resetPassword() {


const response =
await fetch(
    `${API_BASE}/auth/reset-password`,
    {
        method:"POST",

        headers:{
            "Content-Type":
            "application/json"
        },

        body:JSON.stringify({

            email:
            document.getElementById("email").value,

            otp:
            document.getElementById("otp").value,

            new_password:
            document.getElementById("newPassword").value
        })
    }
);

if(response.ok){

    alert(
        "Password Updated Successfully"
    );

    window.location =
    "login.html";
}


}
