// ✅ Real API Prediction
document.getElementById("predictionForm").addEventListener("submit", async function(e){
    e.preventDefault();

    document.getElementById("result").innerText = "Calculating...";
    document.getElementById("result").style.color = "#2a5298";

    const formData = new FormData(document.getElementById("predictionForm"));

    try {
        const response = await fetch("http://127.0.0.1:8000/api/predict", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            const formattedPrice = new Intl.NumberFormat('en-IN', {
                style: 'currency',
                currency: 'INR',
                maximumFractionDigits: 0
            }).format(data.prediction);

            document.getElementById("result").innerText = "Estimated Price: " + formattedPrice;
            document.getElementById("result").style.color = "#2a5298";
        } else {
            document.getElementById("result").innerText = "Error: " + data.error;
            document.getElementById("result").style.color = "red";
        }

    } catch (error) {
        document.getElementById("result").innerText = "Error: Backend server band hai! Pehle python Backend/app.py chalao.";
        document.getElementById("result").style.color = "red";
    }
});

// Chart
const ctx = document.getElementById('priceChart').getContext('2d');

new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Maruti', 'Hyundai', 'Honda', 'Tata', 'Toyota'],
        datasets: [{
            label: 'Average Price',
            data: [350000, 450000, 500000, 400000, 600000],
            backgroundColor: '#2a5298'
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false }
        }
    }
});