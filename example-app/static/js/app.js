// Custom JavaScript for AI Agent Dashboard

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap tooltips are available
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Show result containers when they have content
    function showResult(containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            container.style.display = 'block';
            container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    // Hide result containers
    function hideResult(containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            container.style.display = 'none';
        }
    }

    // Global error handler for fetch requests
    function handleFetchError(error, context) {
        console.error(`Error in ${context}:`, error);
        showNotification('An error occurred. Please check the console for details.', 'error');
    }

    // Notification system
    function showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    // Loading state management
    function setLoading(buttonId, loading = true) {
        const button = document.getElementById(buttonId);
        if (button) {
            button.disabled = loading;
            if (loading) {
                button.dataset.originalText = button.innerHTML;
                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            } else {
                button.innerHTML = button.dataset.originalText || button.innerHTML;
            }
        }
    }

    // Copy to clipboard functionality
    window.copyToClipboard = function(text) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copied to clipboard!', 'success');
        }).catch(() => {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showNotification('Copied to clipboard!', 'success');
        });
    };

    // Format file size
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Format timestamp
    function formatTimestamp(date) {
        return date.toLocaleString();
    }

    // Add to activity log (global function for templates)
    window.addToActivityLog = function(message, type = 'info') {
        const log = document.querySelector('.activity-log');
        if (log) {
            const time = formatTimestamp(new Date());
            const badgeClass = type === 'success' ? 'bg-success' :
                              type === 'error' ? 'bg-danger' :
                              type === 'warning' ? 'bg-warning' : 'bg-info';

            log.innerHTML = `<div class="mb-2">
                <small class="text-muted">${time}</small>
                <span class="badge ${badgeClass} ms-2">${type}</span>
                <div>${message}</div>
            </div>` + log.innerHTML;

            // Keep only last 20 entries
            const entries = log.children;
            while (entries.length > 20) {
                log.removeChild(entries[entries.length - 1]);
            }
        }
    };

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K to focus search (if exists)
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"], input[placeholder*="search" i]');
            if (searchInput) {
                searchInput.focus();
            }
        }

        // Escape to clear results
        if (e.key === 'Escape') {
            const resultContainers = document.querySelectorAll('.result-container[style*="display: block"]');
            resultContainers.forEach(container => {
                container.style.display = 'none';
            });
        }
    });

    // Auto-resize textareas
    document.addEventListener('input', function(e) {
        if (e.target.tagName.toLowerCase() === 'textarea') {
            e.target.style.height = 'auto';
            e.target.style.height = e.target.scrollHeight + 'px';
        }
    });

    // Form validation enhancement
    document.addEventListener('submit', function(e) {
        const form = e.target;
        if (!form.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();

            // Find first invalid field and focus it
            const firstInvalid = form.querySelector(':invalid');
            if (firstInvalid) {
                firstInvalid.focus();
                showNotification('Please fill in all required fields.', 'warning');
            }
        }
        form.classList.add('was-validated');
    });

    // Initialize any existing result containers that should be shown
    document.querySelectorAll('.result-container').forEach(container => {
        if (container.textContent.trim()) {
            container.style.display = 'block';
        }
    });

    console.log('AI Agent Dashboard JavaScript loaded successfully');
});
