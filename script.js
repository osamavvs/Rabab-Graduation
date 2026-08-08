const openButton = document.getElementById("openButton");
const welcomeScreen = document.getElementById("welcomeScreen");
const mainPage = document.getElementById("mainPage");
const confettiContainer = document.getElementById("confetti");


/* فتح الصفحة */

openButton.addEventListener("click", function () {

    welcomeScreen.classList.add("hide");

    mainPage.classList.remove("hidden");

    createConfetti();

    setTimeout(() => {
        welcomeScreen.style.display = "none";
    }, 900);

});


/* مؤثرات التخرج */

function createConfetti() {

    const symbols = [
        "🎓",
        "✨",
        "★",
        "✦",
        "♥"
    ];

    for (let i = 0; i < 80; i++) {

        const piece = document.createElement("div");

        piece.classList.add("confetti");

        piece.innerHTML =
            symbols[Math.floor(Math.random() * symbols.length)];

        piece.style.left =
            Math.random() * 100 + "%";

        piece.style.fontSize =
            (Math.random() * 12 + 8) + "px";

        piece.style.animationDuration =
            (Math.random() * 3 + 3) + "s";

        piece.style.animationDelay =
            Math.random() * 2 + "s";

        confettiContainer.appendChild(piece);

        setTimeout(() => {
            piece.remove();
        }, 7000);

    }

}
