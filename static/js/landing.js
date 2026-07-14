// Scroll animation

const faders = document.querySelectorAll(".fade-in");

window.addEventListener("scroll", () => {
    faders.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight - 100) {
            el.classList.add("visible");
        }
    });
});

// Parallax effect

document.addEventListener("mousemove", (e) => {
    const planet = document.querySelector(".planet");
    const x = (e.clientX / window.innerWidth - 0.5) * 30;
    const y = (e.clientY / window.innerHeight - 0.5) * 30;

    planet.style.transform = `translate(${x}px, ${200 + y}px)`;
});