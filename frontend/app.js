// Configuration: Empty string means it will use the current domain (since backend and frontend are hosted together)
const BACKEND_URL = ''; 


document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('url-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('span');
    const btnLoader = document.getElementById('btn-loader');
    
    const resultContainer = document.getElementById('result-container');
    const shortenedUrlInput = document.getElementById('shortened-url');
    const copyBtn = document.getElementById('copy-btn');
    const copyStatus = document.getElementById('copy-status');
    
    const errorContainer = document.getElementById('error-container');
    const errorMessage = document.getElementById('error-message');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Reset states
        resultContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
        copyStatus.textContent = '';
        
        const originalUrl = document.getElementById('original_url').value.trim();
        const shortCode = document.getElementById('short_code').value.trim();
        
        if (!originalUrl) return;

        // UI Loading state
        submitBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'block';

        try {
            const payload = {
                original_url: originalUrl,
                short_code: shortCode || undefined
            };

            const response = await fetch(`${BACKEND_URL}/api/v1/shorturl/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to shorten URL');
            }

            // Success state
            // Construct the shortened URL. If you have a specific domain for your short links, replace it here.
            const domain = window.location.origin; // Using the current domain for preview
            // Or you can use the backend domain if that handles redirection:
            // const domain = BACKEND_URL;
            
            shortenedUrlInput.value = `${domain}/${data.short_code}`;
            resultContainer.classList.remove('hidden');

        } catch (error) {
            // Error state
            errorMessage.textContent = error.message;
            errorContainer.classList.remove('hidden');
        } finally {
            // Restore UI
            submitBtn.disabled = false;
            btnText.style.display = 'block';
            btnLoader.style.display = 'none';
        }
    });

    copyBtn.addEventListener('click', async () => {
        try {
            await navigator.clipboard.writeText(shortenedUrlInput.value);
            copyStatus.textContent = 'Copied to clipboard!';
            copyStatus.style.color = 'var(--success)';
            
            // Revert icon after 2 seconds
            setTimeout(() => {
                copyStatus.textContent = '';
            }, 2000);
        } catch (err) {
            copyStatus.textContent = 'Failed to copy';
            copyStatus.style.color = 'var(--error)';
        }
    });
});
