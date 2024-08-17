// Function to handle Predict Expenditure form submission
document.getElementById('predict-expenditure-form')?.addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    
    try {
        const response = await fetch('http://127.0.0.1:5000/predict_expenditure', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        const resultBox = document.getElementById('expenditure-result');
        resultBox.innerHTML = `<h2>Predicted expenditure: ${data.predicted_expenditure}</h2>`;
    } catch (error) {
        console.error('Error:', error);
    }
});

// Function to handle Predict Disease form submission
document.getElementById('predict-disease-form')?.addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const fileInput = document.getElementById('leaf_image');
    const formData = new FormData();
    formData.append('leaf_image', fileInput.files[0]);
    
    try {
        const response = await fetch('http://127.0.0.1:5000/predict_disease', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        const resultBox = document.getElementById('disease-result');
        resultBox.innerHTML = `<h2>Predicted disease: ${data.predicted_disease}</h2>`;
    } catch (error) {
        console.error('Error:', error);
    }
});

// Function to handle Get Details form submission
document.getElementById('get-details-form')?.addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    
    try {
        const response = await fetch('http://127.0.0.1:5000/get_details', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        const resultTable = document.getElementById('details-result');
        
        if (data.details && Object.keys(data.details).length > 0) {
            let tableHTML = '<table><thead><tr>';
            for (let key in data.details) {
                tableHTML += `<th>${key}</th>`;
            }
            tableHTML += '</tr></thead><tbody><tr>';
            for (let key in data.details) {
                tableHTML += `<td>${data.details[key]}</td>`;
            }
            tableHTML += '</tr></tbody></table>';
            resultTable.innerHTML = tableHTML;
        } else {
            resultTable.innerHTML = '<p>No details found for the given district and taluk.</p>';
        }
    } catch (error) {
        console.error('Error:', error);
    }
});