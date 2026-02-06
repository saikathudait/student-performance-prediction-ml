(() => {
    const banner = document.getElementById("cookie-banner");
    if (!banner) {
        return;
    }

    const stored = localStorage.getItem("cookie_consent");
    if (stored) {
        banner.classList.add("is-hidden");
        return;
    }

    const acceptBtn = document.getElementById("cookie-accept");
    const declineBtn = document.getElementById("cookie-decline");

    const saveChoice = (value) => {
        localStorage.setItem("cookie_consent", value);
        banner.classList.remove("is-visible");
        setTimeout(() => banner.classList.add("is-hidden"), 250);
    };

    requestAnimationFrame(() => {
        banner.classList.add("is-visible");
    });

    if (acceptBtn) {
        acceptBtn.addEventListener("click", () => saveChoice("accepted"));
    }
    if (declineBtn) {
        declineBtn.addEventListener("click", () => saveChoice("declined"));
    }
})();
