# wdrive - Local Google Drive Server
# Created by: xspoilt-dev
# License: MIT

import os
import logging
import socket
import threading
import time
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, session
from utils.qr_generator import generate_qr_code
from utils.file_manager import FileManager
from utils.logger import setup_logging

# Configuration
UPLOAD_FOLDER = 'shared'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'webp', 'ico',
                      'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm', '3gp', 'mpg', 'mpeg',
                      'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'odt', 'ods', 'odp',
                      'zip', 'rar', '7z', 'tar', 'gz', 'bz2', 'xz',
                      'mp3', 'wav', 'flac', 'aac', 'ogg', 'wma', 'm4a',
                      'html', 'htm', 'css', 'js', 'json', 'xml', 'csv',
                      'py', 'java', 'cpp', 'c', 'cs', 'php', 'rb', 'go',
                      'md', 'rtf', 'log', 'ini', 'cfg', 'conf', 'yml', 'yaml'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 * 1024  # 16GB max file size
SECRET_KEY = 'wdrive-local-server-2025'
PASSWORD_HASH = generate_password_hash('wdrive123')  # Default password

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['SECRET_KEY'] = SECRET_KEY

# Setup logging
logger = setup_logging()
file_manager = FileManager(UPLOAD_FOLDER)

def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        # Connect to a remote address to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        return '127.0.0.1'

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def log_access(request, action, filename=None):
    """Log user access and file operations."""
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'Unknown'))
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"{timestamp} - {client_ip} - {action}"
    if filename:
        log_msg += f" - {filename}"
    logger.info(log_msg)

def require_auth():
    """Check if authentication is required."""
    return 'authenticated' not in session

@app.before_request
def check_auth():
    """Check authentication before each request."""
    if request.endpoint == 'login' or request.endpoint == 'static':
        return
    if require_auth():
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user authentication."""
    if request.method == 'POST':
        password = request.form.get('password')
        if password and check_password_hash(PASSWORD_HASH, password):
            session['authenticated'] = True
            log_access(request, "LOGIN_SUCCESS")
            flash('Successfully logged in!', 'success')
            return redirect(url_for('index'))
        else:
            log_access(request, "LOGIN_FAILED")
            flash('Invalid password!', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('authenticated', None)
    log_access(request, "LOGOUT")
    flash('Successfully logged out!', 'success')
    return redirect(url_for('login'))

@app.route('/')
def index():
    """Main page showing file list."""
    search_query = request.args.get('search', '')
    files = file_manager.get_files(search_query)
    log_access(request, "VIEW_FILES")
    return render_template('index.html', files=files, search_query=search_query)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Handle file upload."""
    if request.method == 'POST':
        logger.info(f"Upload request received from {request.environ.get('REMOTE_ADDR', 'Unknown')}")
        
        if 'files' not in request.files:
            logger.warning("No 'files' field in upload request")
            flash('No file selected!', 'error')
            return redirect(request.url)
        
        files = request.files.getlist('files')
        logger.info(f"Received {len(files)} files for upload")
        uploaded_files = []
        
        for i, file in enumerate(files):
            logger.info(f"Processing file {i+1}: {file.filename}")
            
            if file.filename == '':
                logger.warning(f"File {i+1} has empty filename, skipping")
                continue
                
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                logger.info(f"Saving file to: {filepath}")
                
                # Handle duplicate filenames
                counter = 1
                original_filename = filename
                while os.path.exists(filepath):
                    name, ext = os.path.splitext(original_filename)
                    filename = f"{name}_{counter}{ext}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    counter += 1
                
                try:
                    file.save(filepath)
                    uploaded_files.append(filename)
                    logger.info(f"Successfully saved file: {filename}")
                    log_access(request, "FILE_UPLOAD", filename)
                except Exception as e:
                    logger.error(f"Error uploading file {filename}: {str(e)}")
                    flash(f'Error uploading {filename}!', 'error')
            else:
                logger.warning(f"File type not allowed: {file.filename}")
                flash(f'File type not allowed: {file.filename}', 'error')
        
        logger.info(f"Upload complete. Successfully uploaded {len(uploaded_files)} files")
        if uploaded_files:
            flash(f'Successfully uploaded {len(uploaded_files)} file(s)!', 'success')
        
        return redirect(url_for('index'))
    
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    """Handle file download."""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            log_access(request, "FILE_DOWNLOAD", filename)
            return send_file(filepath, as_attachment=True)
        else:
            flash('File not found!', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Error downloading file {filename}: {str(e)}")
        flash('Error downloading file!', 'error')
        return redirect(url_for('index'))

@app.route('/preview/<filename>')
def preview_file(filename):
    """Handle file preview."""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            log_access(request, "FILE_PREVIEW", filename)
            return send_file(filepath)
        else:
            flash('File not found!', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Error previewing file {filename}: {str(e)}")
        flash('Error previewing file!', 'error')
        return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    """Handle file deletion."""
    try:
        if file_manager.delete_file(filename):
            log_access(request, "FILE_DELETE", filename)
            flash(f'Successfully deleted {filename}!', 'success')
        else:
            flash('File not found!', 'error')
    except Exception as e:
        logger.error(f"Error deleting file {filename}: {str(e)}")
        flash('Error deleting file!', 'error')
    
    return redirect(url_for('index'))

@app.route('/rename/<filename>', methods=['POST'])
def rename_file(filename):
    """Handle file rename."""
    new_name = request.form.get('new_name')
    if not new_name:
        flash('Please provide a new name!', 'error')
        return redirect(url_for('index'))
    
    try:
        new_name = secure_filename(new_name)
        if file_manager.rename_file(filename, new_name):
            log_access(request, "FILE_RENAME", f"{filename} -> {new_name}")
            flash(f'Successfully renamed to {new_name}!', 'success')
        else:
            flash('Error renaming file!', 'error')
    except Exception as e:
        logger.error(f"Error renaming file {filename}: {str(e)}")
        flash('Error renaming file!', 'error')
    
    return redirect(url_for('index'))

@app.route('/api/files')
def api_files():
    """API endpoint to get file list."""
    search_query = request.args.get('search', '')
    files = file_manager.get_files(search_query)
    return jsonify(files)

@app.route('/api/upload-progress')
def upload_progress():
    """API endpoint for upload progress (placeholder)."""
    return jsonify({'progress': 100, 'status': 'complete'})

@app.route('/favicon.ico')
def favicon():
    """Handle favicon requests."""
    return send_file(os.path.join('static', 'favicon.svg'), mimetype='image/svg+xml')

@app.route('/api/debug/files')
def debug_files():
    """Debug endpoint to check files in shared folder."""
    try:
        shared_path = Path(UPLOAD_FOLDER)
        files_info = []
        
        if shared_path.exists():
            for file_path in shared_path.iterdir():
                if file_path.is_file():
                    stat = file_path.stat()
                    files_info.append({
                        'name': file_path.name,
                        'size': stat.st_size,
                        'path': str(file_path),
                        'exists': True
                    })
        
        return jsonify({
            'shared_folder_exists': shared_path.exists(),
            'shared_folder_path': str(shared_path.absolute()),
            'files_count': len(files_info),
            'files': files_info
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_shared_folder():
    """Create the shared folder if it doesn't exist."""
    shared_path = Path(UPLOAD_FOLDER)
    shared_path.mkdir(exist_ok=True)
    logger.info(f"Shared folder ready: {shared_path.absolute()}")

def start_dns_server(local_ip):
    """Start the DNS server in a separate thread."""
    # DNS server disabled - using IP address only
    logger.info("DNS server disabled - using IP address only")
    return False

def main():
    """Main function to start the wdrive server."""
    print("🚀 Starting wdrive - Local Google Drive Server")
    print("=" * 50)
    
    # Create shared folder
    create_shared_folder()
    
    # Get local IP
    local_ip = get_local_ip()
    print(f"📍 Local IP: {local_ip}")
    
    # Start DNS server
    dns_started = start_dns_server(local_ip)
    if dns_started:
        print("🌐 DNS server started - Access via http://wdrive/")
    else:
        print("🌐 Using IP address access only")
    
    # Generate QR code
    server_url = f"http://{local_ip}:8080/"
    qr_path = generate_qr_code(server_url)
    if qr_path:
        print(f"📱 QR code generated: {qr_path}")
        print(f"🔗 Server URL: {server_url}")
    
    # Start Flask app
    port = 8080
    print(f"🌟 Starting Flask server on port {port}")
    print("🔒 Default password: wdrive123")
    print("=" * 50)
    
    try:
        app.run(
            host='0.0.0.0',
            port=8080,
            debug=False,
            threaded=True,
            use_reloader=False
        )
    except PermissionError:
        print("❌ Permission denied for port 8080. Trying port 3000...")
        app.run(
            host='0.0.0.0',
            port=3000,
            debug=False,
            threaded=True,
            use_reloader=False
        )

if __name__ == '__main__':
    main()
