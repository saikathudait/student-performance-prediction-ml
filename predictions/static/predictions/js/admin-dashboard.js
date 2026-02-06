document.addEventListener("DOMContentLoaded", () => {
    const clock = document.getElementById("admin-clock");
    const search = document.getElementById("admin-search");
    const modules = Array.from(document.querySelectorAll("[data-module]"));

    const updateClock = () => {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, "0");
        const minutes = now.getMinutes().toString().padStart(2, "0");
        if (clock) {
            clock.textContent = `${hours}:${minutes}`;
        }
    };

    updateClock();
    setInterval(updateClock, 30000);

    if (search) {
        search.addEventListener("input", (event) => {
            const value = event.target.value.toLowerCase();
            modules.forEach((module) => {
                const text = module.textContent.toLowerCase();
                module.style.display = text.includes(value) ? "" : "none";
            });
        });
    }
});
