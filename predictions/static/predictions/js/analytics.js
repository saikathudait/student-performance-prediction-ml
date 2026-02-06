document.addEventListener("DOMContentLoaded", () => {
    const chartElement = document.getElementById("resultChart");
    const chartDataEl = document.getElementById("chart-data");
    if (!chartElement || !chartDataEl || typeof Chart === "undefined") {
        return;
    }

    const payload = JSON.parse(chartDataEl.textContent);
    const ctx = chartElement.getContext("2d");

    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: payload.labels,
            datasets: [
                {
                    data: payload.values,
                    backgroundColor: ["rgba(22, 163, 74, 0.8)", "rgba(220, 38, 38, 0.8)"],
                    borderWidth: 0,
                },
            ],
        },
        options: {
            plugins: {
                legend: {
                    position: "bottom",
                },
            },
            cutout: "65%",
        },
    });
});
