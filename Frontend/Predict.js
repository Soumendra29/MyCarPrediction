const predictionForm = document.getElementById("predictionForm");
const resultDiv = document.getElementById("result");

if (predictionForm) {
    predictionForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        resultDiv.textContent = "Calculating price...";
        resultDiv.style.opacity = "0.7";
        resultDiv.style.color = "#0f2d59";

        const formData = new FormData(predictionForm);
        const requestUrl = `http://127.0.0.1:8000/api/predict`;

        try {
            const response = await fetch(requestUrl, {
                method: 'POST',
                body: formData
            });
            const responseText = await response.text();
            let data;

            try {
                data = JSON.parse(responseText);
            } catch (parseError) {
                resultDiv.textContent = `Error: server returned invalid response.`;
                resultDiv.style.color = '#b32d2e';
                resultDiv.style.opacity = '1';
                console.error('Invalid JSON response:', responseText);
                return;
            }

            if (response.ok && data.success) {
                const formattedPrice = new Intl.NumberFormat('en-IN', {
                    style: 'currency',
                    currency: 'INR',
                    maximumFractionDigits: 0
                }).format(data.prediction);

                resultDiv.textContent = `Estimated Price: ${formattedPrice}`;
                resultDiv.style.color = '#0f2d59';
                resultDiv.style.opacity = '1';
            } else {
                resultDiv.textContent = `Error: ${data.error || 'Unable to predict'}`;
                resultDiv.style.color = '#b32d2e';
                resultDiv.style.opacity = '1';
            }
        } catch (error) {
            resultDiv.textContent = `Error: Backend server band hai! Pehle python Backend/app.py chalao.`;
            resultDiv.style.color = '#b32d2e';
            resultDiv.style.opacity = '1';
            console.error('Prediction request failed:', error);
        }
    });
}