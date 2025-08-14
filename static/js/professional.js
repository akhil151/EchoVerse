/**
 * EchoVerse Professional JavaScript
 * Extraordinary UI interactions and animations
 */

const ProfessionalEchoVerse = {
    // Configuration
    config: {
        animationDuration: 300,
        scrollThreshold: 100,
        autoHideAlerts: 5000,
        loadingSteps: [
            'Connecting to IBM Granite API...',
            'Initializing LLM services...',
            'Loading AI features...',
            'Preparing TTS engine...',
            'System ready!'
        ]
    },

    // Initialize professional features
    init() {
        this.initScrollEffects();
        this.initAnimations();
        this.initInteractions();
        this.initParticles();
        console.log('🚀 EchoVerse Professional UI initialized');
    },

    // Scroll effects
    initScrollEffects() {
        const navbar = document.querySelector('.professional-nav');
        
        window.addEventListener('scroll', () => {
            if (window.scrollY > this.config.scrollThreshold) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    },

    // Initialize animations
    initAnimations() {
        // Animate elements on scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate__animated', 'animate__fadeInUp');
                }
            });
        }, observerOptions);

        // Observe all cards and sections
        document.querySelectorAll('.professional-card, .hero-section, .feature-section').forEach(el => {
            observer.observe(el);
        });
    },

    // Initialize interactions
    initInteractions() {
        // Professional button hover effects
        document.querySelectorAll('.professional-btn').forEach(btn => {
            btn.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
            });

            btn.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });

        // Card hover effects
        document.querySelectorAll('.professional-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-8px)';
                this.style.boxShadow = 'var(--shadow-xl)';
            });

            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = 'var(--shadow-md)';
            });
        });
    },

    // Initialize particle background
    initParticles() {
        const canvas = document.createElement('canvas');
        canvas.id = 'particles-canvas';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '-1';
        canvas.style.opacity = '0.1';
        
        document.body.appendChild(canvas);
        
        this.animateParticles(canvas);
    },

    // Animate particles
    animateParticles(canvas) {
        const ctx = canvas.getContext('2d');
        const particles = [];
        const particleCount = 50;

        // Resize canvas
        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }

        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        // Create particles
        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 2 + 1
            });
        }

        // Animate particles
        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            particles.forEach(particle => {
                // Update position
                particle.x += particle.vx;
                particle.y += particle.vy;

                // Wrap around edges
                if (particle.x < 0) particle.x = canvas.width;
                if (particle.x > canvas.width) particle.x = 0;
                if (particle.y < 0) particle.y = canvas.height;
                if (particle.y > canvas.height) particle.y = 0;

                // Draw particle
                ctx.beginPath();
                ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                ctx.fillStyle = '#667eea';
                ctx.fill();
            });

            requestAnimationFrame(animate);
        }

        animate();
    },

    // Professional loading with steps
    showSteppedLoading(title = 'Processing...') {
        const overlay = document.getElementById('loadingOverlay');
        const titleEl = document.getElementById('loadingTitle');
        const textEl = document.getElementById('loadingText');
        const progressEl = document.getElementById('loadingProgress');

        if (titleEl) titleEl.textContent = title;
        overlay.classList.add('show');

        let currentStep = 0;
        const totalSteps = this.config.loadingSteps.length;

        const stepInterval = setInterval(() => {
            if (currentStep < totalSteps) {
                textEl.textContent = this.config.loadingSteps[currentStep];
                const progress = ((currentStep + 1) / totalSteps) * 100;
                progressEl.style.width = progress + '%';
                currentStep++;
            } else {
                clearInterval(stepInterval);
            }
        }, 1000);

        return stepInterval;
    },

    // Hide loading overlay
    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        overlay.classList.remove('show');
    },

    // Professional alert system
    showAlert(message, type = 'info', duration = 5000) {
        const container = document.getElementById('alertContainer');
        const alertId = 'alert-' + Date.now();
        
        const icons = {
            success: 'fa-check-circle',
            danger: 'fa-exclamation-triangle',
            warning: 'fa-exclamation-circle',
            info: 'fa-info-circle'
        };

        const alertHtml = `
            <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show professional-alert animate__animated animate__fadeInDown" role="alert">
                <i class="fas ${icons[type]} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;

        container.innerHTML = alertHtml;

        // Auto-dismiss
        if (duration > 0) {
            setTimeout(() => {
                const alert = document.getElementById(alertId);
                if (alert) {
                    alert.classList.add('animate__fadeOutUp');
                    setTimeout(() => {
                        alert.remove();
                    }, 300);
                }
            }, duration);
        }
    },

    // Professional modal system
    showModal(title, content, actions = []) {
        const modalId = 'professional-modal-' + Date.now();
        
        const actionsHtml = actions.map(action => 
            `<button type="button" class="btn ${action.class || 'btn-secondary'} professional-btn" 
                     onclick="${action.onclick || ''}">${action.text}</button>`
        ).join('');

        const modalHtml = `
            <div class="modal fade" id="${modalId}" tabindex="-1">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content professional-card">
                        <div class="modal-header border-0">
                            <h5 class="modal-title gradient-text">${title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            ${content}
                        </div>
                        <div class="modal-footer border-0">
                            ${actionsHtml}
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        const modal = new bootstrap.Modal(document.getElementById(modalId));
        modal.show();

        // Clean up after modal is hidden
        document.getElementById(modalId).addEventListener('hidden.bs.modal', function() {
            this.remove();
        });

        return modal;
    },

    // Professional progress tracking
    createProgressTracker(steps) {
        const trackerId = 'progress-tracker-' + Date.now();
        
        const stepsHtml = steps.map((step, index) => `
            <div class="progress-step" data-step="${index}">
                <div class="step-icon">
                    <i class="fas fa-circle"></i>
                </div>
                <div class="step-content">
                    <div class="step-title">${step.title}</div>
                    <div class="step-description">${step.description}</div>
                </div>
            </div>
        `).join('');

        const trackerHtml = `
            <div id="${trackerId}" class="professional-progress-tracker">
                <div class="progress-line"></div>
                ${stepsHtml}
            </div>
        `;

        return {
            id: trackerId,
            html: trackerHtml,
            updateStep: (stepIndex, status = 'active') => {
                const tracker = document.getElementById(trackerId);
                if (tracker) {
                    const steps = tracker.querySelectorAll('.progress-step');
                    steps.forEach((step, index) => {
                        step.classList.remove('active', 'completed', 'error');
                        if (index < stepIndex) {
                            step.classList.add('completed');
                        } else if (index === stepIndex) {
                            step.classList.add(status);
                        }
                    });
                }
            }
        };
    },

    // Professional form validation
    validateForm(formElement) {
        const inputs = formElement.querySelectorAll('input, textarea, select');
        let isValid = true;

        inputs.forEach(input => {
            const value = input.value.trim();
            const isRequired = input.hasAttribute('required');
            
            // Remove previous validation classes
            input.classList.remove('is-valid', 'is-invalid');
            
            if (isRequired && !value) {
                input.classList.add('is-invalid');
                isValid = false;
            } else if (value) {
                input.classList.add('is-valid');
            }
        });

        return isValid;
    },

    // Professional API helper
    async apiCall(endpoint, options = {}) {
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        };

        const config = { ...defaultOptions, ...options };

        try {
            const response = await fetch(endpoint, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'API request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            this.showAlert(`API Error: ${error.message}`, 'danger');
            throw error;
        }
    },

    // Professional file upload
    handleFileUpload(fileInput, callback) {
        const file = fileInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        // Show upload progress
        const progressHtml = `
            <div class="upload-progress">
                <div class="progress">
                    <div class="progress-bar" style="width: 0%"></div>
                </div>
                <small class="text-muted">Uploading ${file.name}...</small>
            </div>
        `;

        // Create progress element
        const progressEl = document.createElement('div');
        progressEl.innerHTML = progressHtml;
        fileInput.parentNode.appendChild(progressEl);

        // Simulate upload progress
        let progress = 0;
        const progressBar = progressEl.querySelector('.progress-bar');
        
        const progressInterval = setInterval(() => {
            progress += Math.random() * 30;
            if (progress > 90) progress = 90;
            progressBar.style.width = progress + '%';
        }, 200);

        // Make API call
        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            clearInterval(progressInterval);
            progressBar.style.width = '100%';
            
            setTimeout(() => {
                progressEl.remove();
                if (callback) callback(data);
            }, 500);
        })
        .catch(error => {
            clearInterval(progressInterval);
            progressEl.remove();
            this.showAlert('Upload failed: ' + error.message, 'danger');
        });
    },

    // Utility functions
    utils: {
        // Format duration
        formatDuration(minutes) {
            const hours = Math.floor(minutes / 60);
            const mins = Math.floor(minutes % 60);
            
            if (hours > 0) {
                return `${hours}h ${mins}m`;
            } else {
                return `${mins}m`;
            }
        },

        // Format file size
        formatFileSize(bytes) {
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            if (bytes === 0) return '0 Bytes';
            
            const i = Math.floor(Math.log(bytes) / Math.log(1024));
            return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
        },

        // Debounce function
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        // Copy to clipboard
        async copyToClipboard(text) {
            try {
                await navigator.clipboard.writeText(text);
                ProfessionalEchoVerse.showAlert('Copied to clipboard!', 'success', 2000);
            } catch (err) {
                console.error('Failed to copy: ', err);
                ProfessionalEchoVerse.showAlert('Failed to copy to clipboard', 'danger');
            }
        }
    }
};

// Export for global use
window.ProfessionalEchoVerse = ProfessionalEchoVerse;
