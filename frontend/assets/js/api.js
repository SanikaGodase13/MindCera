const API_BASE = "http://127.0.0.1:8000";

console.log(
"MindCera API Connected:",
API_BASE
);

/* =========================
POST REQUEST
========================= */

async function postAPI(
endpoint,
data
) {

```
const res = await fetch(
    API_BASE + endpoint,
    {
        method: "POST",

        headers: {
            "Content-Type":
            "application/json",

            "Authorization":
            "Bearer " +
            localStorage.getItem("token")
        },

        body:
        JSON.stringify(data)
    }
);

return await res.json();
```

}

/* =========================
GET REQUEST
========================= */

async function getAPI(
endpoint
) {


const res = await fetch(
    API_BASE + endpoint,
    {
        method: "GET",

        headers: {
            "Authorization":
            "Bearer " +
            localStorage.getItem("token")
        }
    }
);

return await res.json();


}

/* =========================
DASHBOARD
========================= */

async function getDashboard() {


const res = await fetch(
    `${API_BASE}/dashboard`,
    {
        method: "GET",

        headers: {
            "Authorization":
            "Bearer " +
            localStorage.getItem("token")
        }
    }
);

return await res.json();

}
