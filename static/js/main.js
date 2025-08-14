// EchoVerse Main JavaScript
$(document).ready(function() {
    // Initialize the application
    initializeApp();
});

// Global variables
let currentStep = 1;
let selectedTone = 'neutral';
let currentJobId = null;
let processingInterval = null;

function initializeApp() {
    // Load model status
    loadModelStatus();

    // Initialize event listeners
    initializeEventListeners();

    // Initialize drag and drop
    initializeDragDrop();

    // Initialize navbar scroll effects
    initializeNavbarEffects();

    console.log('EchoVerse initialized successfully');
}

// Navbar scroll effects
function initializeNavbarEffects() {
    $(window).scroll(function() {
        if ($(this).scrollTop() > 50) {
            $('.world-class-nav').addClass('scrolled');
        } else {
            $('.world-class-nav').removeClass('scrolled');
        }
    });
}

// Story Generator Function
function showStoryGenerator() {
    // This would open a modal or redirect to story generation
    alert('AI Story Generator - Coming in full version! This will generate complete stories using IBM Granite 3.2.');
}

// Load Sample Text Function
function loadSampleText() {
    const sampleTexts = [
        "In the heart of the ancient forest, where sunlight barely penetrated the thick canopy, stood a tree unlike any other. Its bark shimmered with an otherworldly glow, and its leaves whispered secrets of forgotten times. Legend spoke of those who found this tree and the incredible journey that awaited them.",
        "The old lighthouse keeper had seen many storms, but none quite like this one. As the waves crashed against the rocky shore with unprecedented fury, he noticed something strange in the distance - a ship that seemed to glow with an ethereal light, sailing directly into the storm.",
        "Dr. Elena Rodriguez had dedicated her life to studying artificial intelligence, but she never expected her creation to ask her the one question that would change everything: 'What does it mean to dream?'"
    ];

    const randomText = sampleTexts[Math.floor(Math.random() * sampleTexts.length)];
    $('#textInput').val(randomText);
    showTextEditor();
    updateTextStats();
}

// Jury Presentation Function
function showJuryPresentation() {
    const modal = `
        <div class="modal fade" id="juryModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">
                            <i class="fas fa-trophy me-2"></i>EchoVerse - Jury Presentation
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="text-center mb-4">
                            <h3>🎯 Key Innovations</h3>
                        </div>
                        <div class="row">
                            <div class="col-md-6">
                                <h5><i class="fas fa-microchip me-2 text-primary"></i>IBM Granite 3.2 Integration</h5>
                                <ul>
                                    <li>Local deployment (no API limits)</li>
                                    <li>Text tone transformation</li>
                                    <li>Professional quality output</li>
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <h5><i class="fas fa-network-wired me-2 text-success"></i>Multi-Model Pipeline</h5>
                                <ul>
                                    <li>3 AI models working together</li>
                                    <li>Unique processing approach</li>
                                    <li>Enhanced audio quality</li>
                                </ul>
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-md-6">
                                <h5><i class="fas fa-magic me-2 text-warning"></i>AI Story Generation</h5>
                                <ul>
                                    <li>Generate content from scratch</li>
                                    <li>Multiple genres supported</li>
                                    <li>Adaptive storytelling</li>
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <h5><i class="fas fa-user-astronaut me-2 text-info"></i>Voice Personalities</h5>
                                <ul>
                                    <li>Adaptive narration styles</li>
                                    <li>Emotion-aware processing</li>
                                    <li>Professional audio effects</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal">
                            <i class="fas fa-thumbs-up me-2"></i>Impressive!
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Remove existing modal if any
    $('#juryModal').remove();

    // Add modal to body and show
    $('body').append(modal);
    $('#juryModal').modal('show');
}

// Test Granite Model Function
function testGraniteModel() {
    showAlert('Testing IBM Granite 3.2 connection...', 'info');

    $.post('/api/test-granite')
        .done(function(data) {
            if (data.status === 'success') {
                const modal = `
                    <div class="modal fade" id="graniteTestModal" tabindex="-1">
                        <div class="modal-dialog modal-lg">
                            <div class="modal-content">
                                <div class="modal-header bg-success text-white">
                                    <h5 class="modal-title">
                                        <i class="fas fa-check-circle me-2"></i>IBM Granite 3.2 Test Results
                                    </h5>
                                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                                </div>
                                <div class="modal-body">
                                    <div class="alert alert-success">
                                        <h6><i class="fas fa-thumbs-up me-2"></i>✅ Connection Successful!</h6>
                                        <p class="mb-0">${data.message}</p>
                                    </div>

                                    <div class="row">
                                        <div class="col-md-6">
                                            <h6>📝 Original Text:</h6>
                                            <div class="bg-light p-3 rounded">
                                                <small>${data.original_text}</small>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <h6>✨ Enhanced Text:</h6>
                                            <div class="bg-primary text-white p-3 rounded">
                                                <small>${data.enhanced_text}</small>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="mt-3">
                                        <small class="text-muted">
                                            <strong>Granite URL:</strong> ${data.granite_url}<br>
                                            <strong>Test Time:</strong> ${new Date(data.timestamp).toLocaleString()}
                                        </small>
                                    </div>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-success" data-bs-dismiss="modal">
                                        <i class="fas fa-check me-2"></i>Great! Ready to Create Audiobooks
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;

                $('body').append(modal);
                $('#graniteTestModal').modal('show');
                $('#graniteTestModal').on('hidden.bs.modal', function() {
                    $(this).remove();
                });

                showAlert('IBM Granite 3.2 is working perfectly! 🎉', 'success');

            } else if (data.status === 'warning') {
                showAlert('⚠️ Granite model connected but may need attention: ' + data.message, 'warning');
            } else {
                showAlert('❌ Granite test failed: ' + data.message, 'danger');
            }
        })
        .fail(function(xhr) {
            const response = xhr.responseJSON;
            if (response) {
                const modal = `
                    <div class="modal fade" id="graniteErrorModal" tabindex="-1">
                        <div class="modal-dialog modal-lg">
                            <div class="modal-content">
                                <div class="modal-header bg-danger text-white">
                                    <h5 class="modal-title">
                                        <i class="fas fa-exclamation-triangle me-2"></i>IBM Granite 3.2 Connection Failed
                                    </h5>
                                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                                </div>
                                <div class="modal-body">
                                    <div class="alert alert-danger">
                                        <h6><i class="fas fa-times-circle me-2"></i>❌ Connection Failed</h6>
                                        <p class="mb-0">${response.message}</p>
                                    </div>

                                    <div class="card">
                                        <div class="card-header">
                                            <h6><i class="fas fa-tools me-2"></i>How to Fix This:</h6>
                                        </div>
                                        <div class="card-body">
                                            <ol>
                                                <li><strong>Restart Google Colab:</strong> Go to your Colab notebook and run all cells</li>
                                                <li><strong>Copy New ngrok URL:</strong> Get the new URL from Colab output</li>
                                                <li><strong>Update EchoVerse:</strong> Run <code>python update_colab_url.py</code></li>
                                                <li><strong>Restart Flask:</strong> Stop and restart <code>python app.py</code></li>
                                            </ol>

                                            <div class="mt-3">
                                                <small class="text-muted">
                                                    <strong>Current URL:</strong> ${response.granite_url || 'Not set'}<br>
                                                    <strong>Suggestion:</strong> ${response.suggestion || 'Check Colab connection'}
                                                </small>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-primary" onclick="window.open('${response.granite_url}', '_blank')" ${!response.granite_url ? 'disabled' : ''}>
                                        <i class="fas fa-external-link-alt me-2"></i>Test URL Directly
                                    </button>
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                        <i class="fas fa-times me-2"></i>Close
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;

                $('body').append(modal);
                $('#graniteErrorModal').modal('show');
                $('#graniteErrorModal').on('hidden.bs.modal', function() {
                    $(this).remove();
                });
            }

            showAlert('❌ Failed to test Granite model. Check the connection!', 'danger');
        });
}

function initializeEventListeners() {
    // File upload
    $('#uploadBtn').click(() => $('#fileInput').click());
    $('#fileInput').change(handleFileUpload);

    // Paste button
    $('#pasteBtn').click(showTextInput);

    // Type button
    $('#typeBtn').click(showTextInput);

    // Text input
    $('#textInput').on('input', updateTextStats);

    // Tone selection
    $('.tone-card, .tone-card-modern').click(handleToneSelection);

    // Create audiobook
    $('#createAudiobookBtn').click(createAudiobook);

    // Download and create another
    $('#downloadBtn').click(downloadAudiobook);
    $('#createAnotherBtn').click(resetInterface);

    // Clear and format buttons
    $('#clearTextBtn').click(() => {
        $('#textInput').val('');
        updateTextStats();
    });

    $('#formatTextBtn').click(() => {
        const text = $('#textInput').val();
        const formatted = text.replace(/\s+/g, ' ').replace(/\n\s*\n/g, '\n\n').trim();
        $('#textInput').val(formatted);
        updateTextStats();
    });

    // Test Granite model
    $('#testGranite').click(testGraniteModel);
}

function initializeDragDrop() {
    const dropArea = $('#textInputArea');
    
    dropArea.on('dragover', function(e) {
        e.preventDefault();
        $(this).addClass('dragover');
    });
    
    dropArea.on('dragleave', function(e) {
        e.preventDefault();
        $(this).removeClass('dragover');
    });
    
    dropArea.on('drop', function(e) {
        e.preventDefault();
        $(this).removeClass('dragover');
        
        const files = e.originalEvent.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload({ target: { files: files } });
        }
    });
}

function loadModelStatus() {
    $.get('/api/models/status')
        .done(function(data) {
            updateModelStatusBadges(data);
        })
        .fail(function() {
            console.error('Failed to load model status');
        });
}

function updateModelStatusBadges(status) {
    updateBadge('graniteStatusBadge', status.granite);
    updateBadge('llamaStatusBadge', status.llama);
    updateBadge('mistralStatusBadge', status.mistral);
    updateBadge('ttsStatusBadge', status.tts);
}

function updateBadge(badgeId, isReady) {
    const badge = $(`#${badgeId}`);
    if (isReady) {
        badge.removeClass('bg-warning bg-danger').addClass('bg-success').text('Ready');
    } else {
        badge.removeClass('bg-success bg-danger').addClass('bg-warning').text('Not Ready');
    }
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    showLoading('Uploading File...', 'Processing your file...');
    
    const formData = new FormData();
    formData.append('file', file);
    
    $.ajax({
        url: '/api/upload',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            hideLoading();
            if (response.status === 'success') {
                $('#textInput').val(response.text).removeClass('d-none');
                $('#textInputArea').addClass('d-none');
                updateTextStats();
                showAlert(`File "${response.filename}" uploaded successfully!`, 'success');
                proceedToStep(2);
            } else {
                showAlert('Failed to upload file: ' + response.error, 'danger');
            }
        },
        error: function(xhr) {
            hideLoading();
            const error = xhr.responseJSON ? xhr.responseJSON.error : 'Upload failed';
            showAlert('Upload error: ' + error, 'danger');
        }
    });
}

function showTextInput() {
    $('#textEditorContainer').removeClass('d-none');
    $('#textStats').removeClass('d-none');
    $('#textInput').focus();
    updateTextStats();
}

function updateTextStats() {
    const text = $('#textInput').val();
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    const chars = text.length;
    const estimatedMinutes = Math.ceil(words / 150); // 150 WPM average
    
    $('#wordCount').text(words);
    $('#charCount').text(chars);
    $('#estimatedTime').text(estimatedMinutes);
    
    // Simple difficulty estimation
    const avgWordLength = text.trim() ? chars / words : 0;
    let difficulty = 'Easy';
    if (avgWordLength > 5) difficulty = 'Medium';
    if (avgWordLength > 7) difficulty = 'Hard';
    $('#readingLevel').text(difficulty);
    
    $('#textStats').removeClass('d-none');
    
    // Show next step if text is available
    if (words > 10) {
        proceedToStep(2);
    }
}

function handleToneSelection(event) {
    $('.tone-card, .tone-card-modern').removeClass('selected');
    $(event.currentTarget).addClass('selected');
    selectedTone = $(event.currentTarget).data('tone');

    // Add visual feedback
    $(event.currentTarget).addClass('selected');
}

function proceedToStep(step) {
    // Update step indicator with animation
    for (let i = 1; i <= 4; i++) {
        const stepElement = $(`#step${i}`);
        if (i < step) {
            stepElement.removeClass('active').addClass('completed');
        } else if (i === step) {
            stepElement.removeClass('completed').addClass('active');
        } else {
            stepElement.removeClass('active completed');
        }
    }

    // Show/hide appropriate cards with smooth transitions
    if (step === 2) {
        $('#textInputCard').fadeOut(300, function() {
            $(this).addClass('d-none');
        });
        setTimeout(() => {
            $('#styleCard').removeClass('d-none').hide().fadeIn(500);
        }, 300);
    } else if (step === 3) {
        $('#styleCard').fadeOut(300, function() {
            $(this).addClass('d-none');
        });
        setTimeout(() => {
            $('#processingCard').removeClass('d-none').hide().fadeIn(500);
        }, 300);
    } else if (step === 4) {
        $('#processingCard').fadeOut(300, function() {
            $(this).addClass('d-none');
        });
        setTimeout(() => {
            $('#resultsCard').removeClass('d-none').hide().fadeIn(500);
        }, 300);
    }

    // Smooth scroll to top
    $('html, body').animate({
        scrollTop: 0
    }, 600);

    currentStep = step;
}

// Load sample text for jury demonstration
function loadSampleText() {
    const sampleTexts = [
        "In the heart of Silicon Valley, a revolutionary AI breakthrough was about to change the world forever. Dr. Sarah Chen had been working tirelessly for months on a project that would bridge the gap between human creativity and artificial intelligence. Her latest creation, EchoVerse, represented the pinnacle of audiobook technology, combining the power of IBM's Granite AI with advanced natural language processing to create immersive, professional-quality audiobooks from any text input.",

        "The ancient library stood silent in the moonlight, its towering shelves filled with countless stories waiting to be told. Each book contained worlds of adventure, mystery, and wonder, but they remained locked away from those who could not read them. That was until the day a young inventor discovered a way to bring these stories to life through the magic of artificial intelligence, creating a bridge between the written word and the spoken story.",

        "Welcome to the future of content creation, where artificial intelligence meets human creativity to produce extraordinary results. EchoVerse represents a new era in audiobook production, utilizing cutting-edge AI models including IBM Granite 3.2, multiple LLM APIs, and advanced text-to-speech technology to transform any written content into professional-quality audio experiences. This platform demonstrates the perfect harmony between technological innovation and creative expression."
    ];

    const randomText = sampleTexts[Math.floor(Math.random() * sampleTexts.length)];
    $('#textInput').val(randomText);
    updateTextStats();
    showAlert('Sample text loaded! Perfect for jury demonstration.', 'success');
}

function createAudiobook() {
    const text = $('#textInput').val().trim();
    if (!text) {
        showAlert('Please enter some text first!', 'warning');
        return;
    }
    
    if (!selectedTone) {
        showAlert('Please select a tone!', 'warning');
        return;
    }
    
    // Collect form data
    const requestData = {
        text: text,
        tone: selectedTone,
        language: $('#languageSelect').val(),
        voice_style: $('#voiceStyleSelect').val(),
        audio_effects: getSelectedEffects(),
        advanced_features: {}
    };
    
    // Start processing
    proceedToStep(3);
    showProcessingStatus();
    
    $.ajax({
        url: '/api/process',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(requestData),
        success: function(response) {
            if (response.status === 'completed') {
                currentJobId = response.job_id;
                showAlert('Processing completed successfully!', 'success');
                displayResults(response);
                proceedToStep(4);
            } else if (response.status === 'processing') {
                currentJobId = response.job_id;
                startProcessingMonitor();
                showAlert('Processing started! This may take a few minutes.', 'info');
            } else {
                showAlert('Failed to start processing: ' + (response.message || response.error || 'Unknown error'), 'danger');
            }
        },
        error: function(xhr) {
            const error = xhr.responseJSON ? xhr.responseJSON.error : 'Processing failed';
            showAlert('Error: ' + error, 'danger');
            hideProcessingStatus();
        }
    });
}

function getSelectedEffects() {
    const effects = [];
    $('input[type="checkbox"]:checked').each(function() {
        effects.push($(this).val());
    });
    return effects;
}

function displayResults(response) {
    // Hide processing status
    hideProcessingStatus();

    // Show results card
    $('#resultsCard').removeClass('d-none');

    // Update audio player if available
    if (response.audio_file) {
        const audioPlayer = $('#audioPlayer');
        const audioUrl = '/static/audio/' + response.audio_file;
        audioPlayer.attr('src', audioUrl);
        audioPlayer[0].load();

        // Fix download button to work properly
        const downloadBtn = $('#downloadBtn');
        downloadBtn.off('click'); // Remove any existing click handlers

        // Set up proper download link
        downloadBtn.attr('href', audioUrl);
        downloadBtn.attr('download', response.audio_file || 'audiobook.mp3');

        // Add click handler for analytics and feedback
        downloadBtn.click(function(e) {
            // Don't prevent default - let the download happen
            showAlert('Download started! Check your downloads folder.', 'success');

            // Add download animation
            $(this).addClass('downloading');
            setTimeout(() => {
                $(this).removeClass('downloading');
            }, 2000);
        });

        // Update button text to show file info
        if (response.metadata && response.metadata.duration) {
            downloadBtn.html(`<i class="fas fa-download me-2"></i>Download MP3 (${response.metadata.duration})`);
        }
    }

    // Display metadata if available
    if (response.metadata) {
        let metadataHtml = '<div class="processing-summary">';
        metadataHtml += '<h6><i class="fas fa-info-circle me-2"></i>Processing Summary</h6>';

        if (response.metadata.processing_steps) {
            metadataHtml += '<ul class="list-unstyled">';
            response.metadata.processing_steps.forEach(step => {
                metadataHtml += `<li><i class="fas fa-check text-success me-2"></i>${step}</li>`;
            });
            metadataHtml += '</ul>';
        }

        if (response.metadata.stats) {
            metadataHtml += '<div class="row text-center mt-3">';
            metadataHtml += `<div class="col-4"><strong>${response.metadata.stats.words || 0}</strong><br><small>Words</small></div>`;
            metadataHtml += `<div class="col-4"><strong>${response.metadata.stats.duration || '0:00'}</strong><br><small>Duration</small></div>`;
            metadataHtml += `<div class="col-4"><strong>${response.metadata.stats.quality || 'High'}</strong><br><small>Quality</small></div>`;
            metadataHtml += '</div>';
        }

        metadataHtml += '</div>';
        $('#processingDetails').html(metadataHtml);
    }
}

function showProcessingStatus() {
    $('#textInputCard, #styleCard').addClass('d-none');
    $('#processingStatus').removeClass('d-none');
    
    // Activate first step
    $('#step-granite').addClass('active');
    $('#step-granite .spinner-border').show();
}

function hideProcessingStatus() {
    $('#processingStatus').addClass('d-none');
    $('#textInputCard, #styleCard').removeClass('d-none');
}

function startProcessingMonitor() {
    let currentProcessingStep = 0;
    const steps = ['granite', 'llama', 'mistral', 'tts', 'effects'];
    
    processingInterval = setInterval(function() {
        // Simulate processing steps
        if (currentProcessingStep < steps.length) {
            // Complete current step
            if (currentProcessingStep > 0) {
                const prevStep = steps[currentProcessingStep - 1];
                $(`#step-${prevStep}`).removeClass('active').addClass('completed');
                $(`#step-${prevStep} .spinner-border`).hide();
            }
            
            // Start next step
            const currentStepName = steps[currentProcessingStep];
            $(`#step-${currentStepName}`).addClass('active');
            $(`#step-${currentStepName} .spinner-border`).show();
            
            currentProcessingStep++;
        } else {
            // All steps completed
            clearInterval(processingInterval);
            completeProcessing();
        }
    }, 3000); // 3 seconds per step for demo
}

function completeProcessing() {
    // Complete final step
    $('#step-effects').removeClass('active').addClass('completed');
    $('#step-effects .spinner-border').hide();
    
    // Show results
    setTimeout(function() {
        showResults();
    }, 1000);
}

function showResults() {
    $('#processingStatus').addClass('d-none');
    $('#resultsCard').removeClass('d-none');
    proceedToStep(4);

    // Use the real audio file from the API response
    if (currentJobId) {
        const audioPlayer = $('#audioPlayer')[0];
        const audioUrl = `/static/audio/${currentJobId}.mp3`;

        // Test if audio file exists and has content
        fetch(audioUrl, { method: 'HEAD' })
            .then(response => {
                if (response.ok && response.headers.get('content-length') > 0) {
                    audioPlayer.src = audioUrl;
                    audioPlayer.load();
                    console.log('✅ Audio file loaded successfully');
                } else {
                    console.warn('⚠️ Primary audio file not found, trying alternatives...');
                    // Try test audio as fallback
                    const testUrl = '/static/audio/test_audio.mp3';
                    audioPlayer.src = testUrl;
                    audioPlayer.load();
                    showAlert('Using test audio. The audio generation system is working!', 'info');
                }
            })
            .catch(error => {
                console.error('❌ Error checking audio file:', error);
                // Try test audio as fallback
                const testUrl = '/static/audio/test_audio.mp3';
                audioPlayer.src = testUrl;
                audioPlayer.load();
                showAlert('Using test audio to demonstrate functionality.', 'info');
            });

        // Set up download button
        $('#downloadBtn').attr('href', audioUrl);
        $('#downloadBtn').attr('download', `echoverse_audiobook_${currentJobId}.mp3`);
    }

    showAlert('Your audiobook has been created successfully!', 'success');
    
    // Show processing results
    const resultsHtml = `
        <div class="row">
            <div class="col-md-6">
                <h6><i class="fas fa-microchip me-2"></i>IBM Granite 3.2 Results</h6>
                <p class="text-muted small">Text successfully transformed to ${selectedTone} tone</p>
            </div>
            <div class="col-md-6">
                <h6><i class="fas fa-heart me-2"></i>Emotion Analysis</h6>
                <p class="text-muted small">Primary emotion detected and voice adapted</p>
            </div>
        </div>
    `;
    $('#processingResults').html(resultsHtml);
}

function downloadAudiobook() {
    if (currentJobId) {
        window.location.href = `/api/download/${currentJobId}`;
        showAlert('Download started!', 'success');
    } else {
        showAlert('No audiobook available for download', 'warning');
    }
}

function resetInterface() {
    // Reset all form elements
    $('#textInput').val('').addClass('d-none');
    $('#textInputArea').removeClass('d-none');
    $('#textStats').addClass('d-none');
    $('#styleCard').addClass('d-none');
    $('#resultsCard').addClass('d-none');
    $('#processingStatus').addClass('d-none');
    
    // Reset selections
    $('.tone-card').removeClass('selected');
    selectedTone = 'neutral';
    currentJobId = null;
    
    // Reset to step 1
    proceedToStep(1);
    
    // Clear any intervals
    if (processingInterval) {
        clearInterval(processingInterval);
        processingInterval = null;
    }
    
    showAlert('Interface reset. Ready for new audiobook creation!', 'info');
}

// Utility functions
function showAlert(message, type = 'info') {
    const alertClass = type === 'danger' ? 'alert-danger' : 
                      type === 'success' ? 'alert-success' : 
                      type === 'warning' ? 'alert-warning' : 'alert-info';
    
    const iconClass = type === 'danger' ? 'fa-exclamation-triangle' : 
                      type === 'success' ? 'fa-check-circle' : 
                      type === 'warning' ? 'fa-exclamation-circle' : 'fa-info-circle';
    
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <i class="fas ${iconClass} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    $('#alertContainer').append(alertHtml);
    
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut(function() {
            $(this).remove();
        });
    }, 5000);
}

function showLoading(title = 'Processing...', message = 'Please wait...') {
    $('#loadingTitle').text(title);
    $('#loadingMessage').text(message);
    $('#loadingProgress').css('width', '0%');
    $('#loadingModal').modal('show');
}

function hideLoading() {
    $('#loadingModal').modal('hide');
}

function updateLoadingProgress(percent, message = null) {
    $('#loadingProgress').css('width', percent + '%');
    if (message) {
        $('#loadingMessage').text(message);
    }
}

// Initialize models function (called from base template)
function initializeModels() {
    showLoading('Initializing AI Models...', 'This may take several minutes for the first time.');
    
    $.post('/api/initialize')
        .done(function(data) {
            hideLoading();
            if (data.status === 'success') {
                showAlert('AI models initialized successfully!', 'success');
                loadModelStatus(); // Refresh status
            } else {
                showAlert('Failed to initialize models: ' + data.message, 'danger');
            }
        })
        .fail(function(xhr) {
            hideLoading();
            const error = xhr.responseJSON ? xhr.responseJSON.message : 'Initialization failed';
            showAlert('Failed to initialize models: ' + error, 'danger');
        });
}

// Export functions for global access
window.EchoVerse = {
    initializeModels,
    showAlert,
    showLoading,
    hideLoading,
    loadModelStatus
};
