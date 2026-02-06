document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("exam-form");
    const timerEl = document.getElementById("exam-timer");
    if (!form || !timerEl) {
        return;
    }

    const duration = Number(timerEl.dataset.duration || 0);
    let remaining = duration;

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60).toString().padStart(2, "0");
        const secs = Math.floor(seconds % 60).toString().padStart(2, "0");
        return `${mins}:${secs}`;
    };

    const tick = () => {
        if (remaining <= 0) {
            form.submit();
            return;
        }
        timerEl.textContent = formatTime(remaining);
        remaining -= 1;
        setTimeout(tick, 1000);
    };

    timerEl.textContent = formatTime(remaining);
    setTimeout(tick, 1000);

    form.addEventListener("submit", (event) => {
        const questions = form.querySelectorAll(".question-card");
        let unanswered = 0;
        questions.forEach((card) => {
            const checked = card.querySelector("input[type='radio']:checked");
            if (!checked) {
                unanswered += 1;
            }
        });

        if (unanswered > 0) {
            const confirmSubmit = window.confirm(
                `You have ${unanswered} unanswered question(s). Submit anyway?`
            );
            if (!confirmSubmit) {
                event.preventDefault();
            }
        }
    });

    window.addEventListener("beforeunload", (event) => {
        event.preventDefault();
        event.returnValue = "";
    });

    const blockAction = (event) => {
        event.preventDefault();
    };

    form.addEventListener("copy", blockAction);
    form.addEventListener("paste", blockAction);
    form.addEventListener("cut", blockAction);
});
