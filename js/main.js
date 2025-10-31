// Navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const contentSections = document.querySelectorAll('.content-section');

    // Function to switch sections
    function switchSection(targetSection) {
        // Hide all sections
        contentSections.forEach(section => {
            section.classList.remove('active');
        });

        // Show target section
        const targetElement = document.getElementById(targetSection);
        if (targetElement) {
            targetElement.classList.add('active');
        }

        // Update active nav button
        navButtons.forEach(button => {
            button.classList.remove('active');
            if (button.getAttribute('data-target') === targetSection) {
                button.classList.add('active');
            }
        });
    }

    // Add click event listeners to nav buttons
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetSection = this.getAttribute('data-target');
            switchSection(targetSection);
        });
    });

    // Set home as default active section
    switchSection('home');
});

// Simple form validation for future contact form
function validateForm(formData) {
    const errors = [];
    
    if (!formData.name || formData.name.trim() === '') {
        errors.push('Name is required');
    }
    
    if (!formData.email || !isValidEmail(formData.email)) {
        errors.push('Valid email is required');
    }
    
    if (!formData.message || formData.message.trim() === '') {
        errors.push('Message is required');
    }
    
    return errors;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Utility function for making API calls (for future CMS integration)
async function fetchData(endpoint) {
    try {
        const response = await fetch(endpoint);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching data:', error);
        return null;
    }
}

// Image lazy loading for better performance
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.getAttribute('data-src');
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// Try loading HEIC; if the browser can't decode it, use a fallback image.
async function tryLoadHEIC(imgElement, heicPath, fallbackPath) {
    try {
        const resp = await fetch(heicPath);
        if (!resp.ok) throw new Error('fetch failed');
        const blob = await resp.blob();
        // Try to create an ImageBitmap from the blob (will fail if HEIC not supported)
        await createImageBitmap(blob);
        // If successful, use object URL so the browser decodes the HEIC blob directly
        imgElement.src = URL.createObjectURL(blob);
    } catch (err) {
        // Fallback to a supported format
        imgElement.src = fallbackPath;
        console.warn('HEIC not supported or failed to load, using fallback:', err);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeLazyLoading();
});

document.addEventListener('DOMContentLoaded', function() {
    const heicImg = document.getElementById('heic-img');
    if (heicImg) {
        tryLoadHEIC(heicImg, 'media/IMG_1931.HEIC', 'media/image.png');
    }
});