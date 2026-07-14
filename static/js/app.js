const aura = document.getElementById("aura");
const face = document.getElementById("face");
const eyes = document.querySelectorAll(".eye");
const overlay = document.getElementById("system-overlay");
const glyphText = document.getElementById("glyph-text");

let idleTimer;

/* Wakanda Glyph Map */
const glyphMap = {
    A:"ᚨ",B:"ᛒ",C:"ᚲ",D:"ᛞ",E:"ᛖ",F:"ᚠ",G:"ᚷ",H:"ᚺ",
    I:"ᛁ",J:"ᛃ",K:"ᚲ",L:"ᛚ",M:"ᛗ",N:"ᚾ",O:"ᛟ",P:"ᛈ",
    Q:"ᛩ",R:"ᚱ",S:"ᛊ",T:"ᛏ",U:"ᚢ",V:"ᚡ",W:"ᚹ",X:"ᛪ",
    Y:"ᚤ",Z:"ᛉ"
};

/* Convert to glyph */
function toGlyph(text) {
    return text.toUpperCase().split("").map(c => glyphMap[c] || c).join("");
}

/* Splash */
window.addEventListener("load", () => {
    const splash = document.getElementById("splash-screen");
    const mainApp = document.getElementById("main-app");

    // Let splash breathe for 4 seconds
    setTimeout(() => {

        splash.style.transition = "opacity 1.2s ease";
        splash.style.opacity = "0";

        setTimeout(() => {
            splash.remove();
            mainApp.classList.remove("hidden");
        }, 1200);

    }, 4000); // ← Cinematic delay
});

/* Eye tracking */
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

/* Idle */
function resetIdle() {
    clearTimeout(idleTimer);
    face.classList.remove("sleep");

    idleTimer = setTimeout(() => {
        face.classList.add("sleep");
    }, 30000);
}

resetIdle();

/* Show overlay */
function showOverlay(text) {
    glyphText.textContent = toGlyph(text);
    overlay.classList.remove("hidden");
}

function hideOverlay() {
    overlay.classList.add("hidden");
}

/* Chat */
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

    showOverlay("System Processing");

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    });

    const data = await response.json();

    hideOverlay();

    face.classList.remove("thinking");
    face.classList.add("talking");

    chatBox.innerHTML += `<p><strong>AyAstra:</strong> ${data.reply}</p>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    setTimeout(() => {
        face.classList.remove("talking");
        aura.classList.remove("active");
    }, 1500);
}