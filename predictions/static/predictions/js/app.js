document.addEventListener("DOMContentLoaded", () => {
    const revealElements = document.querySelectorAll("[data-reveal]");
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.15 }
    );

    revealElements.forEach((el) => observer.observe(el));

    const filterInput = document.getElementById("record-filter");
    const tableBody = document.getElementById("records-body");
    if (filterInput && tableBody) {
        filterInput.addEventListener("input", (event) => {
            const value = event.target.value.toLowerCase();
            const rows = Array.from(tableBody.querySelectorAll("tr"));
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
