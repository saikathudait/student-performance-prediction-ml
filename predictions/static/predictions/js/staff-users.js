document.addEventListener("DOMContentLoaded", () => {
    const clock = document.getElementById("staff-clock");
    const search = document.getElementById("user-search");
    const rows = Array.from(document.querySelectorAll("#user-table-body tr"));

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
            rows.forEach((row) => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(value) ? "" : "none";
            });
        });
    }
});
