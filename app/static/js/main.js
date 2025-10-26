// Load model information on page load
async function loadModelInfo() {
    try {
        const response = await fetch('/model-info');
        const data = await response.json();
        
        const infoDiv = document.getElementById('model-info');
        
        if (data.model_loaded) {
            infoDiv.innerHTML = `
                <div class="info-item">
                    <strong>Status:</strong> 
                    <span class="status-badge status-success">Model Loaded ✓</span>
                </div>
                <div class="info-item">
                    <strong>Features:</strong> ${data.feature_count}
                </div>
                <div class="info-item">
                    <strong>Model Type:</strong> Random Forest Regressor
                </div>
            `;
        } else {
            infoDiv.innerHTML = `
                <div class="info-item">
                    <strong>Status:</strong> 
                    <span class="status-badge status-error">Model Not Loaded ✗</span>
                </div>
            `;
        }
    } catch (error) {
        document.getElementById('model-info').innerHTML = `
            <div class="error-box">Error loading model info</div>
        `;
    }
}

// Load model metrics
async function loadMetrics() {
    try {
        const response = await fetch('/metrics');
        const data = await response.json();
        
        const metricsDiv = document.getElementById('metrics-display');
        
        if (response.ok) {
            metricsDiv.innerHTML = `
                <div class="metric-item">
                    <span class="metric-label">R² Score:</span>
                    <span class="metric-value">${data.r2.toFixed(4)}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Mean Squared Error:</span>
                    <span class="metric-value">${data.mse.toFixed(2)}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Mean Absolute Error:</span>
                    <span class="metric-value">${data.mae.toFixed(2)}</span>
                </div>
            `;
        }
    } catch (error) {
        document.getElementById('metrics-display').innerHTML = `
            <div class="error-box">Metrics not available</div>
        `;
    }
}

// Handle prediction form submission
document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {};
    
    // Convert all fields to integers
    formData.forEach((value, key) => {
        data[key] = parseInt(value);
    });
    
    console.log('Sending prediction request:', data);
    
    const resultBox = document.getElementById('prediction-result');
    const errorBox = document.getElementById('error-message');
    
    // Hide previous results
    resultBox.style.display = 'none';
    errorBox.style.display = 'none';
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        
        const result = await response.json();
        
        if (response.ok) {
            const predictedValue = Math.round(result.prediction);
            document.getElementById('predicted-value').textContent = predictedValue;
            resultBox.style.display = 'block';
            console.log('Prediction successful:', predictedValue);
        } else {
            errorBox.textContent = `Error: ${result.error}`;
            errorBox.style.display = 'block';
            console.error('Prediction failed:', result.error);
        }
    } catch (error) {
        errorBox.textContent = `Error: ${error.message}`;
        errorBox.style.display = 'block';
        console.error('Request failed:', error);
    }
});

// Load data when page loads
window.addEventListener('DOMContentLoaded', () => {
    loadModelInfo();
    loadMetrics();
});
