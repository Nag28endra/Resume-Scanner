// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const jobDescription = document.getElementById('jobDescription');
const scanButton = document.getElementById('scanButton');
const loading = document.getElementById('loading');
const results = document.getElementById('results');

// File handling
let uploadedFiles = [];

// API base URL - adjust if your API is on a different port
const API_BASE = 'http://localhost:8000';

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupFileUpload();
    setupFormSubmission();
});

// File upload setup
function setupFileUpload() {
    // Click to browse
    uploadArea.addEventListener('click', () => fileInput.click());

    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleFileDrop);
}

function handleFileSelect(event) {
    const files = Array.from(event.target.files);
    processFiles(files);
}

function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleFileDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');

    const files = Array.from(event.dataTransfer.files);
    processFiles(files);
}

function processFiles(files) {
    const validFiles = files.filter(file => {
        const ext = file.name.split('.').pop().toLowerCase();
        return ['pdf', 'docx', 'txt'].includes(ext);
    });

    if (validFiles.length === 0) {
        showError('Please select PDF, DOCX, or TXT files only.');
        return;
    }

    uploadedFiles = validFiles;
    displayFileList(validFiles);
    uploadFiles(validFiles);
}

function displayFileList(files) {
    fileList.innerHTML = '';

    files.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <span class="file-name">${file.name}</span>
            <span class="file-status" id="status-${index}">Uploading...</span>
        `;
        fileList.appendChild(fileItem);
    });
}

async function uploadFiles(files) {
    const formData = new FormData();

    files.forEach(file => {
        formData.append('files', file);
    });

    try {
        const response = await fetch(`${API_BASE}/api/upload`, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            // Update file statuses
            files.forEach((file, index) => {
                const statusElement = document.getElementById(`status-${index}`);
                statusElement.textContent = 'Uploaded';
                statusElement.className = 'file-status success';
                document.getElementById(`status-${index}`).parentElement.classList.add('success');
            });

            showSuccess(`Successfully uploaded ${result.total} resume(s)`);
        } else {
            throw new Error(result.detail || 'Upload failed');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showError('Failed to upload files: ' + error.message);

        // Update file statuses to error
        files.forEach((file, index) => {
            const statusElement = document.getElementById(`status-${index}`);
            statusElement.textContent = 'Failed';
            statusElement.className = 'file-status error';
            document.getElementById(`status-${index}`).parentElement.classList.add('error');
        });
    }
}

// Form submission setup
function setupFormSubmission() {
    scanButton.addEventListener('click', handleScan);
}

async function handleScan() {
    const description = jobDescription.value.trim();

    if (!description) {
        showError('Please enter a job description.');
        return;
    }

    if (uploadedFiles.length === 0) {
        showError('Please upload some resumes first.');
        return;
    }

    // Show loading
    scanButton.disabled = true;
    loading.style.display = 'flex';
    results.innerHTML = '';

    try {
        const response = await fetch(`${API_BASE}/api/score`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                job_description: description,
                top_k: 5
            })
        });

        const scoredResults = await response.json();

        if (response.ok) {
            displayResults(scoredResults);
        } else {
            throw new Error(scoredResults.detail || 'Scoring failed');
        }
    } catch (error) {
        console.error('Scoring error:', error);
        showError('Failed to score resumes: ' + error.message);
    } finally {
        // Hide loading
        scanButton.disabled = false;
        loading.style.display = 'none';
    }
}

function displayResults(scoredResults) {
    if (scoredResults.length === 0) {
        results.innerHTML = '<p class="no-results">No results found.</p>';
        return;
    }

    results.innerHTML = '';

    scoredResults.forEach(result => {
        const resultCard = document.createElement('div');
        resultCard.className = 'result-card';

        resultCard.innerHTML = `
            <div class="result-header">
                <div class="result-file">${result.file_name}</div>
                <div class="result-score ${result.decision.toLowerCase().replace(' ', '-')}">
                    ${result.final_score}/100 - ${result.decision}
                </div>
            </div>
            <div class="result-details">
                <div class="detail-item">
                    <span class="detail-label">Semantic Match:</span>
                    <span class="detail-value">${(result.semantic_score * 100).toFixed(1)}%</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Skills Match:</span>
                    <span class="detail-value">${(result.skill_score * 100).toFixed(1)}%</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Experience Match:</span>
                    <span class="detail-value">${(result.experience_score * 100).toFixed(1)}%</span>
                </div>
            </div>
            <div class="result-reason">${result.reason}</div>
        `;

        results.appendChild(resultCard);
    });
}

// Utility functions
function showSuccess(message) {
    showMessage(message, 'success');
}

function showError(message) {
    showMessage(message, 'error');
}

function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());

    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;

    // Insert at top of container
    const container = document.querySelector('.container');
    container.insertBefore(messageDiv, container.firstChild);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 5000);
}