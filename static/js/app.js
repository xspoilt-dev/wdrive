// wdrive JavaScript functionality
class WDriveApp {
    constructor() {
        this.init();
    }

    init() {
        this.setupServiceWorker();
        this.setupNotifications();
        this.setupKeyboardShortcuts();
        this.setupAutoRefresh();
        this.setupTooltips();
    }

    // Service Worker for PWA functionality
    setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/sw.js')
                .then(registration => {
                    console.log('ServiceWorker registered:', registration);
                })
                .catch(error => {
                    console.log('ServiceWorker registration failed:', error);
                });
        }
    }

    // Browser notifications
    setupNotifications() {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }

    // Keyboard shortcuts
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+U for upload
            if (e.ctrlKey && e.key === 'u') {
                e.preventDefault();
                window.location.href = '/upload';
            }
            // Ctrl+H for home
            if (e.ctrlKey && e.key === 'h') {
                e.preventDefault();
                window.location.href = '/';
            }
            // Escape to close modals
            if (e.key === 'Escape') {
                const modals = document.querySelectorAll('.modal.show');
                modals.forEach(modal => {
                    const bsModal = bootstrap.Modal.getInstance(modal);
                    if (bsModal) bsModal.hide();
                });
            }
        });
    }

    // Auto-refresh file list
    setupAutoRefresh() {
        if (window.location.pathname === '/') {
            setInterval(() => {
                this.refreshFileList();
            }, 30000); // Refresh every 30 seconds
        }
    }

    // Bootstrap tooltips
    setupTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Refresh file list without page reload
    async refreshFileList() {
        try {
            const response = await fetch('/api/files');
            if (response.ok) {
                const files = await response.json();
                this.updateFileList(files);
            }
        } catch (error) {
            console.error('Failed to refresh file list:', error);
        }
    }

    // Update file list in DOM
    updateFileList(files) {
        const filesList = document.getElementById('filesList');
        if (!filesList) return;

        // This would need to recreate the file list HTML
        // For simplicity, we'll just show a notification
        this.showNotification('File list updated', 'info');
    }

    // Show toast notifications
    showNotification(message, type = 'info') {
        const toastContainer = this.getToastContainer();
        const toastId = 'toast-' + Date.now();
        
        const toastHTML = `
            <div id="${toastId}" class="toast align-items-center text-white bg-${type === 'error' ? 'danger' : (type === 'success' ? 'success' : 'primary')}" role="alert">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="bi bi-${this.getIconForType(type)} me-2"></i>
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        
        toastContainer.insertAdjacentHTML('beforeend', toastHTML);
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
        
        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }

    getToastContainer() {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
        }
        return container;
    }

    getIconForType(type) {
        switch (type) {
            case 'success': return 'check-circle-fill';
            case 'error': return 'exclamation-triangle-fill';
            case 'warning': return 'exclamation-triangle-fill';
            default: return 'info-circle-fill';
        }
    }

    // File operations
    async uploadFiles(files, progressCallback) {
        const formData = new FormData();
        Array.from(files).forEach(file => {
            formData.append('files', file);
        });

        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();

            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable && progressCallback) {
                    const progress = (e.loaded / e.total) * 100;
                    progressCallback(progress);
                }
            });

            xhr.addEventListener('load', () => {
                if (xhr.status === 200) {
                    resolve(xhr.response);
                } else {
                    reject(new Error('Upload failed'));
                }
            });

            xhr.addEventListener('error', () => {
                reject(new Error('Upload failed'));
            });

            xhr.open('POST', '/upload');
            xhr.send(formData);
        });
    }

    // Utility functions
    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }

    copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                this.showNotification('Copied to clipboard', 'success');
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showNotification('Copied to clipboard', 'success');
        }
    }

    // Network status monitoring
    setupNetworkMonitoring() {
        window.addEventListener('online', () => {
            this.showNotification('Connection restored', 'success');
        });

        window.addEventListener('offline', () => {
            this.showNotification('Connection lost - working offline', 'warning');
        });
    }

    // Theme switching
    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-bs-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    }

    loadTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-bs-theme', savedTheme);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.wdriveApp = new WDriveApp();
});

// Global utility functions
function shareFile(filename, url) {
    if (navigator.share) {
        navigator.share({
            title: `Shared from wdrive: ${filename}`,
            url: url
        }).catch(err => console.log('Error sharing:', err));
    } else {
        // Fallback: copy link to clipboard
        window.wdriveApp.copyToClipboard(url);
    }
}

function downloadFile(filename) {
    const link = document.createElement('a');
    link.href = `/download/${encodeURIComponent(filename)}`;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// File type detection
function getFileIcon(filename) {
    const extension = filename.split('.').pop().toLowerCase();
    const iconMap = {
        // Images
        'jpg': 'bi-file-earmark-image',
        'jpeg': 'bi-file-earmark-image',
        'png': 'bi-file-earmark-image',
        'gif': 'bi-file-earmark-image',
        'svg': 'bi-file-earmark-image',
        'webp': 'bi-file-earmark-image',
        
        // Videos
        'mp4': 'bi-file-earmark-play',
        'avi': 'bi-file-earmark-play',
        'mov': 'bi-file-earmark-play',
        'mkv': 'bi-file-earmark-play',
        'webm': 'bi-file-earmark-play',
        
        // Audio
        'mp3': 'bi-file-earmark-music',
        'wav': 'bi-file-earmark-music',
        'flac': 'bi-file-earmark-music',
        'ogg': 'bi-file-earmark-music',
        
        // Documents
        'pdf': 'bi-file-earmark-pdf',
        'doc': 'bi-file-earmark-word',
        'docx': 'bi-file-earmark-word',
        'xls': 'bi-file-earmark-excel',
        'xlsx': 'bi-file-earmark-excel',
        'ppt': 'bi-file-earmark-ppt',
        'pptx': 'bi-file-earmark-ppt',
        'txt': 'bi-file-earmark-text',
        
        // Archives
        'zip': 'bi-file-earmark-zip',
        'rar': 'bi-file-earmark-zip',
        '7z': 'bi-file-earmark-zip',
        'tar': 'bi-file-earmark-zip',
        'gz': 'bi-file-earmark-zip',
        
        // Code
        'html': 'bi-file-earmark-code',
        'css': 'bi-file-earmark-code',
        'js': 'bi-file-earmark-code',
        'py': 'bi-file-earmark-code',
        'java': 'bi-file-earmark-code',
        'cpp': 'bi-file-earmark-code',
        'c': 'bi-file-earmark-code',
    };
    
    return iconMap[extension] || 'bi-file-earmark';
}

// Drag and drop enhancement
function enhanceDragDrop() {
    let dragCounter = 0;
    
    document.addEventListener('dragenter', function(e) {
        e.preventDefault();
        dragCounter++;
        if (e.dataTransfer.types.includes('Files')) {
            document.body.classList.add('drag-active');
        }
    });
    
    document.addEventListener('dragleave', function(e) {
        e.preventDefault();
        dragCounter--;
        if (dragCounter === 0) {
            document.body.classList.remove('drag-active');
        }
    });
    
    document.addEventListener('dragover', function(e) {
        e.preventDefault();
    });
    
    document.addEventListener('drop', function(e) {
        e.preventDefault();
        dragCounter = 0;
        document.body.classList.remove('drag-active');
        
        if (e.dataTransfer.files.length > 0 && window.location.pathname === '/') {
            // Redirect to upload page with files
            const files = Array.from(e.dataTransfer.files);
            sessionStorage.setItem('pendingFiles', JSON.stringify(files.map(f => ({ name: f.name, size: f.size }))));
            window.location.href = '/upload';
        }
    });
}

// Initialize drag and drop when page loads
document.addEventListener('DOMContentLoaded', enhanceDragDrop);
