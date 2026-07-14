const blob = document.getElementById("blob");
const eyes = document.querySelectorAll(".eye");
const brows = document.querySelectorAll(".eyebrow");
const mouth = document.querySelector(".mouth");

/* Cursor tracking */

document.addEventListener("mousemove", (e) => {
    const rect = blob.getBoundingClientRect();
    const centerX = rect.left + rect.width/2;
    const centerY = rect.top + rect.height/2;

    const dx = (e.clientX - centerX)/40;
    const dy = (e.clientY - centerY)/40;

    eyes.forEach(eye => {
        eye.style.transform = `translate(${dx}px, ${dy}px)`;
    });
});

/* Click ripple + wobble */

blob.addEventListener("click", () => {
    blob.classList.add("wobble");
    blob.classList.add("clicked");

    setTimeout(() => {
        blob.classList.remove("wobble");
        blob.classList.remove("clicked");
    }, 600);
});

/* Emotion states */

function setEmotion(state) {
    blob.classList.remove("happy", "angry", "sleepy");
    blob.classList.add(state);
}

/* Demo emotion cycle */

setInterval(() => {
    const emotions = ["happy", "angry", "sleepy"];
    const random = emotions[Math.floor(Math.random()*emotions.length)];
    setEmotion(random);
}, 8000);

/* Voice Input */

let audioContext;
let analyser;
let mic;

async function initMic() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    audioContext = new AudioContext();
    analyser = audioContext.createAnalyser();
    mic = audioContext.createMediaStreamSource(stream);
    mic.connect(analyser);
    analyser.fftSize = 256;
    monitorVolume();
}

function monitorVolume() {
    const dataArray = new Uint8Array(analyser.frequencyBinCount);

    function update() {
        analyser.getByteFrequencyData(dataArray);
        let volume = dataArray.reduce((a,b) => a+b) / dataArray.length;

        mouth.style.height = 10 + volume/20 + "px";

        requestAnimationFrame(update);
    }

    update();
}

initMic();