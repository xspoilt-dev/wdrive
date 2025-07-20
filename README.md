# wdrive - Local Google Drive Server

**wdrive** is a complete open-source Python project that creates a local Google Drive-like server on your Wi-Fi network. Built with Flask, it allows you to easily share files between devices without needing internet connectivity.

## ✨ Features

### 🚀 Core Features
- **File Upload & Download**: Drag-and-drop interface with progress tracking
- **File Management**: View, rename, delete files with a beautiful web interface
- **Search & Filter**: Find files quickly by name or type
- **Multi-device Access**: Works on phones, tablets, laptops via web browser
- **PWA Support**: Install as an app on mobile devices

### 🔒 Security & Performance
- **Password Protection**: Configurable authentication
- **Multi-threaded**: Fast concurrent uploads/downloads
- **Large File Support**: Handle files up to 16GB
- **Access Logging**: Track all file operations with timestamps

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- Windows/macOS/Linux

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/xspoilt-dev/wdrive.git
   cd wdrive
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python run.py
   ```

4. **Access the server:**
   - Open `http://127.0.0.1:8080` in your browser
   - Or use the generated QR code on mobile
   - Default password: `wdrive123`

## 🎯 Usage

### Starting the Server

**Basic usage:**
```bash
python run.py
```

**With custom options:**
```bash
python run.py --host 0.0.0.0 --port 8080 --password mypassword
```

**Available options:**
- `--host HOST`: Host address (default: 0.0.0.0)
- `--port PORT`: Port number (default: 8080) 
- `--password PWD`: Custom password
- `--debug`: Enable debug mode
- `--config FILE`: Use config file

### Accessing from Devices

1. **Desktop/Laptop:** `http://[YOUR-IP]:8080/`
2. **Mobile:** Scan the QR code displayed when server starts
3. **Same Network:** All devices must be on the same Wi-Fi network

## 📱 Mobile PWA Installation

1. Open the wdrive website on your mobile browser
2. Look for "Add to Home Screen" or "Install App" option
3. Follow the prompts to install
4. Access wdrive like a native app!

## 🗂 Project Structure

```
wdrive/
├── app.py                 # Main Flask application
├── run.py               # Server startup script
├── requirements.txt     # Python dependencies
├── config.ini          # Configuration file
├── utils/              # Utility modules
│   ├── __init__.py
│   ├── file_manager.py  # File operations
│   ├── logger.py       # Logging utilities
│   └── qr_generator.py # QR code generation
├── templates/          # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html      # File listing page
│   ├── login.html      # Authentication page
│   └── upload.html     # File upload page
├── static/            # Static assets
│   ├── css/
│   ├── js/
│   ├── favicon.svg
│   ├── manifest.json  # PWA manifest
│   └── sw.js         # Service worker
├── shared/           # Upload directory (auto-created)
└── logs/            # Log files (auto-created)
```

## ⚙️ Configuration

### Config File (`config.ini`)
```ini
[server]
host = 0.0.0.0
port = 8080
debug = false

[security]
require_auth = true
max_file_size = 17179869184  # 16 GB

[features]
enable_dns_server = true
enable_qr_code = true
enable_file_preview = true
```

### Environment Variables
- `WDRIVE_PASSWORD`: Set default password
- `WDRIVE_PORT`: Set default port
- `WDRIVE_HOST`: Set default host

### File Upload Features
- **Drag & Drop**: Drop files directly onto the webpage
- **Multi-file**: Upload multiple files simultaneously
- **Progress Tracking**: Real-time upload progress
- **Auto-rename**: Prevents filename conflicts
- **Type Validation**: Configurable file type restrictions

### File Management
- **Preview**: View images, videos, PDFs in browser
- **Search**: Find files by name or extension
- **Filtering**: Filter by file type (images, documents, etc.)
- **Bulk Operations**: Select and manage multiple files

## 📊 Supported File Types

- **Images**: JPG, PNG, GIF, SVG, WebP, BMP
- **Videos**: MP4, AVI, MOV, MKV, WebM, WMV
- **Audio**: MP3, WAV, FLAC, AAC, OGG, WMA
- **Documents**: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX
- **Text**: TXT, MD, RTF, HTML, CSS, JS, Python
- **Archives**: ZIP, RAR, 7Z, TAR, GZ
- **And many more...**

## 🚀 Building Standalone Executable

Create a portable executable with PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" run.py
```

The executable will be in the `dist/` directory.

## 🔐 Security Considerations

- **Local Network Only**: Server binds to local network interfaces
- **Password Protection**: Configurable authentication required
- **File Validation**: Configurable file type restrictions
- **Access Logging**: All operations are logged with IP addresses
- **No Internet Required**: Completely offline operation

## 🐛 Troubleshooting

### Common Issues

**Permission Denied (Port 53/80):**
- Run as administrator/root
- Use alternative ports (8080, 3000, etc.)

**Cannot Access from Mobile:**
- Ensure all devices are on same Wi-Fi network
- Check firewall settings
- Try IP address instead of 'wdrive' domain

**Upload Fails:**
- Check file size limits (16GB max by default)
- Verify file type is allowed
- Ensure sufficient disk space


### Performance Tips

- Use SSD storage for better performance
- Increase `max_file_size` if needed
- Monitor `logs/wdrive.log` for issues
- Use wired network for fastest transfers

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest features.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask**: Web framework
- **Bootstrap**: UI framework
- **Bootstrap Icons**: Icon library
- **qrcode**: QR code generation

## 📧 Contact

**Telegram**: x_spoilt

---

⭐ **Star this repository if you find it useful!**

🐛 **Found a bug?** [Report it here](https://github.com/xspoilt-dev/wdrive/issues)

💡 **Have an idea?** [Suggest a feature](https://github.com/xspoilt-dev/wdrive/issues)
