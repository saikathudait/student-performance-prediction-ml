document.addEventListener("DOMContentLoaded", () => {
    const clock = document.getElementById("staff-clock");
    const search = document.getElementById("staff-search");
    const rows = Array.from(document.querySelectorAll("#staff-table-body tr"));

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
                const nameCell = row.querySelector("td");
                if (!nameCell) {
                    return;
                }
                const matches = nameCell.textContent.toLowerCase().includes(value);
                row.style.display = matches ? "" : "none";
            });
        });
    }
});
