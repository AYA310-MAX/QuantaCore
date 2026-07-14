const aura = document.getElementById("aura");
const face = document.getElementById("face");
const eyes = document.querySelectorAll(".eye");

let idleTimer;

/* SPLASH */
window.addEventListener("load", () => {
    setTimeout(() => {
        document.getElementById("splash-screen").style.opacity = "0";
        document.getElementById("splash-screen").style.transition = "opacity 1s ease";

        setTimeout(() => {
            document.getElementById("splash-screen").remove();
            document.getElementById("main-app").classList.remove("hidden");
        }, 1000);

    }, 3000);
});

/* EYE TRACK */
document.addEventListener("mousemove", (e) => {
    const rect = face.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    const deltaX = (e.clientX - centerX) / 30;
    const deltaY = (e.clientY - centerY) / 30;

    eyes.forEach(eye => {
        eye.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
    });

    resetIdle();
});

/* IDLE SYSTEM */

function resetIdle() {
    clearTimeout(idleTimer);
    face.classList.remove("sleep");

    idleTimer = setTimeout(() => {
        face.classList.add("sleep");
    }, 30000);
}

resetIdle();

/* CHAT */

async function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const message = input.value;
    if (!message) return;

    chatBox.innerHTML += `<p><strong>You:</strong> ${message}</p>`;
    input.value = "";

    face.classList.remove("sleep");
    face.classList.add("thinking");
    aura.classList.add("active");

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    });

    const data = await response.json();

    face.classList.remove("thinking");
    face.classList.add("talking");

    chatBox.innerHTML += `<p><strong>AyAstra:</strong> ${data.reply}</p>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    setTimeout(() => {
        face.classList.remove("talking");
        aura.classList.remove("active");
    }, 1500);
}