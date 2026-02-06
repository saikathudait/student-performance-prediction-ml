document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("student-form");
    if (!form) {
        return;
    }

    const g1Input = form.querySelector("#id_g1");
    const g2Input = form.querySelector("#id_g2");
    const absInput = form.querySelector("#id_absences");
    const liveG1 = document.getElementById("live-g1");
    const liveG2 = document.getElementById("live-g2");
    const liveAbs = document.getElementById("live-absences");
    const progressBar = document.getElementById("score-progress");

    const updateSnapshot = () => {
        const g1 = Number(g1Input?.value || 0);
        const g2 = Number(g2Input?.value || 0);
        const abs = Number(absInput?.value || 0);

        if (liveG1) liveG1.textContent = g1 || 0;
        if (liveG2) liveG2.textContent = g2 || 0;
        if (liveAbs) liveAbs.textContent = abs || 0;

        const avgScore = Math.max(0, Math.min(20, (g1 + g2) / 2));
        const percentage = (avgScore / 20) * 100;
        if (progressBar) {
            progressBar.style.width = `${percentage}%`;
        }
    };

    [g1Input, g2Input, absInput].forEach((input) => {
        if (input) {
            input.addEventListener("input", updateSnapshot);
        }
    });

    updateSnapshot();

    const errorBox = document.getElementById("form-errors");
    const rangeInputs = form.querySelectorAll("[data-min][data-max]");

    form.addEventListener("submit", (event) => {
        const errors = [];

        rangeInputs.forEach((input) => {
            const value = input.value.trim();
            const min = Number(input.dataset.min);
            const max = Number(input.dataset.max);
            const numeric = Number(value);

            if (value === "" || Number.isNaN(numeric)) {
                errors.push(`${input.name} is required.`);
                input.classList.add("input-error");
                return;
            }

            if (numeric < min || numeric > max) {
                errors.push(`${input.name} must be between ${min} and ${max}.`);
                input.classList.add("input-error");
            } else {
                input.classList.remove("input-error");
            }
        });

        if (errors.length) {
            event.preventDefault();
            if (errorBox) {
                errorBox.innerHTML = `<p>${errors[0]}</p>`;
            }
            return;
        }

        const confirmed = window.confirm("Submit this data to generate a prediction?");
        if (!confirmed) {
            event.preventDefault();
        }
    });
});
